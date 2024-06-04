#!/usr/bin/python
from merlin2_mission import Merlin2FsmMissionNode
from merlin2_hospital_patrolling.pddl import room_at, room_patrolled, room_type
from merlin2_basic_actions.merlin2_basic_types import wp_type

from kant_dto import PddlObjectDto, PddlConditionEffectDto, PddlPropositionDto
from merlin2_basic_actions.merlin2_basic_predicates import robot_at
from yasmin import Blackboard
from yasmin_ros.basic_outcomes import SUCCEED
from yasmin import CbState

import rclpy

class MissionNode(Merlin2FsmMissionNode):
    
    END = "end"
    HAS_NEXT = "has_next"

    def __init__(self):

        super().__init__("mission_node")

        self.add_state(
            "PREPARING_GOALS",
            CbState([SUCCEED], self.prepare_goals),
            transitions = {
                SUCCEED: "CHECKING_GOALS"
            }
        )

        self.add_state(
            "CHECKING_GOALS",
            CbState([self.END, self.HAS_NEXT], self.check_goals),
            transitions={
                self.END: SUCCEED,
                self.HAS_NEXT: "EXECUTING_PATROL",
            }
        )

        self.add_state(
            "EXECUTING_PATROL",
            CbState([SUCCEED], self.execute_patrol),
            transitions = {
                SUCCEED: "CHECKING_GOALS"
            }
        )

    def execute_patrol(self, blackboard):
        
        next_goal = blackboard.next_goal

        self.execute_goal(next_goal)

        return SUCCEED

    def check_goals(self, blackboard):
        if blackboard.goals:
            blackboard.next_goal = blackboard.goals.pop(0)
            return self.HAS_NEXT
    
        return self.END



    def create_objects(self):
        
        self.wp0 = PddlObjectDto(wp_type, "wp0")
        self.wp1 = PddlObjectDto(wp_type, "wp1")
        self.wp2 = PddlObjectDto(wp_type, "wp2")
        self.wp3 = PddlObjectDto(wp_type, "wp3")
        self.wp4 = PddlObjectDto(wp_type, "wp4")
        self.wp5 = PddlObjectDto(wp_type, "wp5")

        self.room1 = PddlObjectDto(room_type, "room1")
        self.room2 = PddlObjectDto(room_type, "room2")
        self.room3 = PddlObjectDto(room_type, "room3")
        self.room4 = PddlObjectDto(room_type, "room4")
        self.room5 = PddlObjectDto(room_type, "room5")

        return [
            self.wp0,
            self.wp1,
            self.wp2,
            self.wp3,
            self.wp4,
            self.wp5,
            self.room1,
            self.room2,
            self.room3,
            self.room4,
            self.room5,
        ]
    

    def create_propositions(self):

        self.robot_at_wp0 = PddlPropositionDto(robot_at, [self.wp0])

        self.room1_at_wp1 = PddlPropositionDto(room_at, [self.room1, self.wp1])
        self.room1_at_wp2 = PddlPropositionDto(room_at, [self.room2, self.wp2])
        self.room1_at_wp3 = PddlPropositionDto(room_at, [self.room3, self.wp3])
        self.room1_at_wp4 = PddlPropositionDto(room_at, [self.room4, self.wp4])
        self.room1_at_wp5 = PddlPropositionDto(room_at, [self.room5, self.wp5])


        return [
            self.robot_at_wp0, 
            self.room1_at_wp1,
            self.room1_at_wp2,
            self.room1_at_wp3,
            self.room1_at_wp4,
            self.room1_at_wp5,
        ]
    
    def prepare_goals(self, blackboard):
        blackboard.goals = [
            PddlPropositionDto(room_patrolled, [self.room1], is_goal=True),
            PddlPropositionDto(room_patrolled, [self.room2], is_goal=True),
            PddlPropositionDto(room_patrolled, [self.room3], is_goal=True),
            PddlPropositionDto(room_patrolled, [self.room4], is_goal=True),
            PddlPropositionDto(room_patrolled, [self.room5], is_goal=True),
        ]
        # problem.pddl
        return SUCCEED
    
def main():

    rclpy.init()

    node = MissionNode()

    node.execute_mission()

    node.join_spin()
    rclpy.shutdown()

if __name__ == "__main__":

    main()