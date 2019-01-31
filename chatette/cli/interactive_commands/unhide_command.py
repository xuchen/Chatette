"""
Module `chatette.cli.interactive_commands.unhide_command`.
Contains the strategy class that represents the interacive mode command
`unhide` which restores a unit definition that has been hidden.
"""

from chatette.cli.interactive_commands.command_strategy import CommandStrategy
from chatette.cli.interactive_commands.hide_command import HideCommand


class UnhideCommand(CommandStrategy):
    def __init__(self, command_str):
        super(UnhideCommand, self).__init__(command_str)

    def execute(self, facade):
        """
        Implements the command `unhide` which restores a unit definition that
        was hidden from the parser of `facade`.
        """
        if len(self.command_tokens) > 3:
            self.print_wrapper.error_log("Missing some arguments\nUsage: " +
                                         'unhide <unit-type> "<unit-name>"')
            return
        
        unit_type = CommandStrategy.get_unit_type_from_str(self.command_tokens[1])
        unit_name = CommandStrategy.remove_quotes(self.command_tokens[2])
        try:
            unit = HideCommand.stored_units[unit_type.name][unit_name]
            facade.parser.add_definition(unit_type, unit_name, unit)
            del HideCommand.stored_units[unit_type.name][unit_name]
            self.print_wrapper.write(unit_type.name.capitalize() + " '" +
                                     unit_name + "' was successfully restored.")
        except KeyError:
            self.print_wrapper.write(unit_type.name.capitalize() + " '" +
                                     unit_name + "' was not previously hidden.")
        except ValueError:
            self.print_wrapper.write(unit_type.name.capitalize() + " '" +
                                     unit_name + "' is already defined " +
                                     "the parser.")
