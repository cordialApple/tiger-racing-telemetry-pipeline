from parser.aim_parser import AimParser
from parser.base import ParserRegistry
from parser.canlog_parser import CanLogParser


def default_registry() -> ParserRegistry:
    return ParserRegistry([AimParser(), CanLogParser()])
