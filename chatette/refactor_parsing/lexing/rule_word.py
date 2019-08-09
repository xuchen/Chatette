# coding: utf-8
"""
Module `chatette.refactor_parsing.lexing.rule_word`
Contains the definition of the class that represents the lexing rule
to tokenize a word (inside a rule).
"""

from chatette.refactor_parsing.lexing.lexing_rule import LexingRule
from chatette.refactor_parsing.lexing import LexicalToken, TerminalType
from chatette.refactor_parsing.utils import \
    ESCAPEMENT_SYM, \
    FILE_INCLUSION_SYM, \
    UNIT_START_SYM, UNIT_END_SYM, \
    ALIAS_SYM, SLOT_SYM, INTENT_SYM, \
    SLOT_VAL_SYM, \
    CHOICE_START, CHOICE_END, CHOICE_SEP, \
    OLD_CHOICE_START, OLD_CHOICE_END, OLD_CHOICE_SEP, \
    RAND_GEN_SYM, \
    find_unescaped, find_next_comment
from chatette.utils import min_if_exist


class RuleWord(LexingRule):
    _should_be_escaped_chars = [
        FILE_INCLUSION_SYM,
        UNIT_START_SYM, UNIT_END_SYM,
        ALIAS_SYM, SLOT_SYM, INTENT_SYM,
        SLOT_VAL_SYM,
        # CHOICE_START, CHOICE_END, 
        OLD_CHOICE_START, OLD_CHOICE_END
    ]
    _should_be_escaped_in_choices_chars = [
        # CHOICE_SEP,
        OLD_CHOICE_SEP,
        RAND_GEN_SYM
    ]

    def _apply_strategy(self, **kwargs):
        """
        `kwargs` can contain a boolean with key `inside_choice` that is
        `True` when the current word is inside a choice and `False` otherwise.
        If this boolean is not in `kwargs`, defaults to `False`.
        """
        inside_choice = kwargs.get("inside_choice", False)

        # TODO this might be better using regexes
        if self._text[self._start_index].isspace():
            self.error_msg = \
                "Invalid token. Expected a word instead of a whitespace there."
            return False

        # Find whitespace after the word
        end_word_index = self._start_index
        while True:
            if end_word_index == len(self._text):
                break
            if self._text[end_word_index].isspace():
                end_word_index -= 1
                break
            end_word_index += 1
        
        end_word_index = \
            min_if_exist(
                end_word_index,
                find_next_comment(self._text, self._start_index)
            )

        if end_word_index == self._start_index:
            self.error_msg = "Invalid token. Expected a word to start here."
            return False
        for current_char in RuleWord._should_be_escaped_chars:
            if end_word_index == self._start_index + 1:
                break
            end_word_index = \
                min_if_exist(
                    end_word_index,
                    find_unescaped(self._text, current_char, self._start_index)
                )
        
        if end_word_index > self._start_index + 1 and inside_choice:
            for choice_sep_char in RuleWord._should_be_escaped_in_choices_chars:
                end_word_index = \
                    min_if_exist(
                        end_word_index,
                        find_unescaped(
                            self._text, choice_sep_char, self._start_index
                        )
                    )

        if end_word_index == self._start_index:
            self.error_msg = "Invalid token. Expected a word to start here."
            return False

        word = self._text[self._start_index:end_word_index + 1]
        self._next_index = end_word_index + 1
        print("word is " + word + " then '" + self._text[end_word_index+1:] + "'")
        self._tokens.append(LexicalToken(TerminalType.word, word))
        return True
