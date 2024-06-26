#!/usr/bin/python
from merlin2_hospital_patrolling.pddl import room_at, room_patrolled, room_type
from merlin2_basic_actions.merlin2_basic_types import wp_type
from merlin2_basic_actions.merlin2_basic_predicates import robot_at
from merlin2_fsm_action import Merlin2BasicStates

from kant_dto import PddlObjectDto, PddlConditionEffectDto

from merlin2_fsm_action import Merlin2FsmAction
from yasmin import Blackboard
from yasmin_ros.basic_outcomes import SUCCEED
from yasmin import CbState
import rclpy
from geometry_msgs.msg import Twist
import time

class Merlin2RoomPatrolFSMAction(Merlin2FsmAction):

    def __init__(self):
        
        self._room = PddlObjectDto(room_type, "room")
        self._wp = PddlObjectDto(wp_type, "wp")
        super().__init__("room_patrol_action_node")
        
        self.publisher = self.create_publisher(Twist, 'cmd_vel', 10)

        

        tts_state = self.create_state(Merlin2BasicStates.TTS)
        # falta estado de girar -> usar el cmdvel y publicar pa q gire y esperar

        self.add_state(
            "START_SPIN",
            CbState([SUCCEED], self.rotate),
            transitions={
                SUCCEED:"PREPARING_TEXT"
            }
        )

        self.add_state(
            "PREPARING_TEXT",
            CbState([SUCCEED], self.prepare_text),
            transitions={
                SUCCEED:"SPEAKING"
            }
        )

        self.add_state(
            "SPEAKING",
            tts_state
        )

        # una accion tiene efectos, condiciones y parámetros
        
    def rotate(self, blackboard) -> str:
        self.get_logger().info("LLEGUE A ROTATE")
        rate = self.create_rate(10)  # 10 Hz

        for _ in range(50): 
            # girar durante 5 segundos
            twist_msg = Twist()
            twist_msg.angular.z = 1.0
            self.publisher.publish(twist_msg)
            rate.sleep()

        for _ in range(50):  # Esperar 5 segundos
            rate.sleep()

        twist_msg.angular.z = 0.0
        self.publisher.publish(twist_msg)

        return SUCCEED


    def prepare_text(self, blackboard)->str:
        # room_name = blackboard.merlin2_action_goal.objects[0][-1]

        blackboard.text = "Girado" # room patrolled

        self.get_logger().info("LLEGUE A PREPARE_TEXT")

        return SUCCEED

    def create_parameters(self):
        return [self._room, self._wp]
    
    def create_conditions(self):

        # cond_1 = PddlConditionEffectDto(
        #     room_patrolled,
        #     [self._room],
        #     PddlConditionEffectDto.AT_START,
        #     is_negative = True
        # )

        cond_2 = PddlConditionEffectDto(
            robot_at,
            [self._wp],
            PddlConditionEffectDto.AT_START
        )

        cond_3 = PddlConditionEffectDto(
            room_at,
            [self._room, self._wp],
            PddlConditionEffectDto.AT_START
        )
        
        return [cond_2, cond_3]
    
    def create_efects(self):

        effect_1 = PddlConditionEffectDto(
            room_patrolled,
            [self._room],
            PddlConditionEffectDto.AT_END,
        )

        return [effect_1]



def main():

    rclpy.init()

    node = Merlin2RoomPatrolFSMAction()

    node.join_spin()
    rclpy.shutdown()

if __name__ == "__main__":

    main()