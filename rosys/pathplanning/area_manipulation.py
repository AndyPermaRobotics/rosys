import uuid
from enum import Enum
from typing import Optional

from nicegui import binding, ui
from nicegui.events import SceneClickEventArguments, SceneDragEventArguments

from .. import rosys
from ..event import Event
from ..geometry import LineSegment, Point
from .area import Area
from .path_planner import PathPlanner


class AreaManipulationMode(Enum):
    IDLE = None
    EDIT = 'Edit'
    DELETE = 'Delete'

# TODO
# - allow removing points from existing areas
# - create areas of different types/colors
# - allow adjusting the sphere size
# - translation


class Translator:
    Edit = 'Edit'
    Delete = 'Delete'
    Cancel = 'Cancel'
    Done = 'Done'
    Undo = 'Undo'


class AreaManipulation:
    mode = binding.BindableProperty(on_change=lambda sender, value: sender.MODE_CHANGED.emit(value))

    def __init__(self, path_planner: PathPlanner, translator: Optional[Translator] = None) -> None:
        self.path_planner = path_planner
        self.active_area: Optional[Area] = None
        self.mode = AreaManipulationMode.IDLE
        self.translator = translator or Translator()

        self.MODE_CHANGED = Event()
        """the mode has changed (argument: new mode)"""

    def create_ui(self) -> ui.row:
        t = self.translator
        with ui.row() as row:
            area_toggle = ui.toggle({
                AreaManipulationMode.EDIT: t.Edit,
                AreaManipulationMode.DELETE: t.Delete,
            }).props('outline').bind_value(self, 'mode')
            ui.button(icon='close', on_click=self.cancel) \
                .props('outline') \
                .tooltip(t.Cancel) \
                .bind_visibility_from(area_toggle, 'value', value=AreaManipulationMode.EDIT)
            ui.button(icon='done', on_click=self.done) \
                .props('outline') \
                .tooltip(t.Done) \
                .bind_visibility_from(area_toggle, 'value', bool)
            ui.button(icon='undo', on_click=self.undo) \
                .props('outline') \
                .tooltip(t.Undo) \
                .bind_visibility_from(self, 'can_undo')
        return row

    @property
    def can_undo(self) -> bool:
        return self.active_area is not None and len(self.active_area.outline) > 0

    def add_point(self, point: Point) -> None:
        if self.active_area is None:
            area = Area(id=str(uuid.uuid4()), outline=[], closed=False)
            self.path_planner.areas[area.id] = area
            self.active_area = area

        if self._would_cause_self_intersection(point, self.active_area.outline):
            rosys.notify('Edges must not intersect!', type='negative')
            return

        self.active_area.outline.append(point)
        self._emit_change_event()

    def delete_area(self, point: Point) -> None:
        for area in self.path_planner.areas.values():
            if area.contains(point):
                self.path_planner.areas.pop(area.id)
                self.active_area = None
                self._emit_change_event()
                return
        if not self.path_planner.areas:
            self.mode = AreaManipulationMode.IDLE

    def undo(self) -> None:
        if not self.can_undo:
            return
        assert self.active_area is not None
        self.active_area.outline.pop()
        if not self.active_area.outline:
            self.path_planner.areas.pop(self.active_area.id)
            self.active_area = None
        self._emit_change_event()

    def cancel(self) -> None:
        if self.active_area:
            self.path_planner.areas.pop(self.active_area.id)
            self._emit_change_event()
        self.active_area = None
        self.mode = AreaManipulationMode.IDLE

    def done(self) -> None:
        if self.active_area:
            if len(self.active_area.outline) < 3:
                rosys.notify('Areas must have at least 3 points!', type='negative')
                return
            if self._would_cause_self_intersection(self.active_area.outline[0], self.active_area.outline[1:]):
                rosys.notify('Edges must not intersect!', type='negative')
                return
            self.active_area.closed = True
            self._emit_change_event()
        self.active_area = None
        self.mode = AreaManipulationMode.IDLE

    def handle_click(self, e: SceneClickEventArguments) -> None:
        if e.click_type == 'dblclick':
            for hit in e.hits:
                if hit.object_id == 'ground':
                    target = Point(x=hit.x, y=hit.y)
                    if self.mode == AreaManipulationMode.EDIT:
                        self.add_point(target)
                    elif self.mode == AreaManipulationMode.DELETE:
                        self.delete_area(target)

    def handle_drag_end(self, e: SceneDragEventArguments) -> None:
        _, area_id, type_, point_index = e.object_name.split('_')
        assert area_id in self.path_planner.areas
        area = self.path_planner.areas[area_id]
        if type_ == 'corner':
            area.outline[int(point_index)].x = e.x
            area.outline[int(point_index)].y = e.y
        elif type_ == 'mid':
            area.outline.insert(int(point_index) + 1, Point(x=e.x, y=e.y))
        self._emit_change_event()

    def _emit_change_event(self) -> None:
        self.path_planner.AREAS_CHANGED.emit(self.path_planner.areas)
        self.path_planner.invalidate()

    def _would_cause_self_intersection(self, point: Point, polyline: list[Point]) -> bool:
        if polyline:
            new_edge = LineSegment(point1=polyline[-1], point2=point)
            for i in range(len(polyline) - 2):
                edge = LineSegment(point1=polyline[i], point2=polyline[i + 1])
                if edge.intersect(new_edge):
                    return True
        return False