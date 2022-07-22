from rosys.actors.pathplanning.planner_process import PlannerSearchCommand
from rosys.world import Area, Point, Pose

cmd = PlannerSearchCommand(
    deadline=1657783451.6148303,
    areas=[
        Area(
            id='efc3d76a-dc4f-4578-9dba-b1b673dc63b2', type=None, color='green',
            outline=[Point(x=6.149937727671209, y=-0.17711484789623144),
                     Point(x=9.612772529615507, y=-0.31516119913314),
                     Point(x=27.620256939642154, y=-0.10576934579104247),
                     Point(x=28.024465321296177, y=-2.101078143446283),
                     Point(x=11.736482388608621, y=-3.2472106100020364),
                     Point(x=12.238609367234528, y=-10.776575490209341),
                     Point(x=10.11621581471781, y=-10.751731291418032),
                     Point(x=10.152396176357877, y=-9.206962519468602),
                     Point(x=8.472012560929896, y=-8.997343306897463),
                     Point(x=6.073736496768359, y=-9.22290741066599),
                     Point(x=6.3645103740315045, y=-2.9410622155322494),
                     Point(x=-3.591146169525701, y=-1.6898632678909316),
                     Point(x=-4.920823257785388, y=-1.55630811794593),
                     Point(x=-5.308848849799811, y=0.8671983402731452),
                     Point(x=-2.9936880571586912, y=0.6627623167125547),
                     Point(x=-2.6516373786854417, y=0.20550412900243087),
                     Point(x=0.7800699032359328, y=-0.05897928686265175),
                     Point(x=1.0264402756201714, y=0.2055041290024313)]),
        Area(id='20c09f0d-eb4e-4bfd-a038-7613e7ee815c', type='sand', color='SandyBrown', outline=[]),
        Area(
            id='6e11cb8c-157e-4fc3-8f57-f436eaea5916', type='sand', color='SandyBrown',
            outline=[Point(x=-4.3338589415073905, y=0.20550412900243176),
                     Point(x=-4.1978165476055125, y=-1.537132009177664),
                     Point(x=5.222304593122139, y=-2.5157240058194037),
                     Point(x=5.598362079180236, y=-0.6088155869472143)]),
        Area(
            id='f9777f5e-8b58-4f24-94b6-6379aeca12b4', type='sand', color='SandyBrown',
            outline=[Point(x=26.981890753032665, y=-0.3263875500272597),
                     Point(x=11.664895239366887, y=-0.8104581416677199),
                     Point(x=14.080928558308386, y=-2.5807959888852743),
                     Point(x=26.2813145841394, y=-1.9524768591532027)])],
    obstacles=[],
    start=Pose(
        x=0.5050162048835956, y=-1.6844343414747884, yaw=-3.132945871135351, time=1657783441.6119301),
    goal=Pose(x=-2.0705826461450285, y=-1.1370770520609557, yaw=2.792526803190927, time=0))

robot_outline = [(-0.22, -0.36), (1.07, -0.36), (1.17, 0), (1.07, 0.36), (-0.22, 0.36)]
