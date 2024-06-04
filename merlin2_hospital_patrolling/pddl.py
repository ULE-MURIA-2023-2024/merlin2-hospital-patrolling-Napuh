#!/usr/bin/python
from merlin2_basic_actions.merlin2_basic_types import wp_type
from kant_dto import PddlTypeDto, PddlPredicateDto

#wp_type = PddlTypeDto("wp")
room_type = PddlTypeDto("room")
#predicado que define si una habitacion ha sido patrullada
room_patrolled = PddlPredicateDto("room_patrolled", [room_type])
# indicar donde estan las habitaciones
room_at = PddlPredicateDto("room_at", [room_type, wp_type])
