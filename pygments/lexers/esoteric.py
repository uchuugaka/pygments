# -*- coding: utf-8 -*-
"""
    pygments.lexers.esoteric
    ~~~~~~~~~~~~~~~~~~~~~~~~

    Lexers for esoteric languages.

    :copyright: Copyright 2006-2015 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

from pygments.lexer import RegexLexer, include, words
from pygments.token import Text, Comment, Operator, Keyword, Name, String, \
    Number, Punctuation, Error

__all__ = ['BrainfuckLexer', 'BefungeLexer', 'RedcodeLexer', 'CAmkESLexer']


class BrainfuckLexer(RegexLexer):
    """
    Lexer for the esoteric `BrainFuck <http://www.muppetlabs.com/~breadbox/bf/>`_
    language.
    """

    name = 'Brainfuck'
    aliases = ['brainfuck', 'bf']
    filenames = ['*.bf', '*.b']
    mimetypes = ['application/x-brainfuck']

    tokens = {
        'common': [
            # use different colors for different instruction types
            (r'[.,]+', Name.Tag),
            (r'[+-]+', Name.Builtin),
            (r'[<>]+', Name.Variable),
            (r'[^.,+\-<>\[\]]+', Comment),
        ],
        'root': [
            (r'\[', Keyword, 'loop'),
            (r'\]', Error),
            include('common'),
        ],
        'loop': [
            (r'\[', Keyword, '#push'),
            (r'\]', Keyword, '#pop'),
            include('common'),
        ]
    }


class BefungeLexer(RegexLexer):
    """
    Lexer for the esoteric `Befunge <http://en.wikipedia.org/wiki/Befunge>`_
    language.

    .. versionadded:: 0.7
    """
    name = 'Befunge'
    aliases = ['befunge']
    filenames = ['*.befunge']
    mimetypes = ['application/x-befunge']

    tokens = {
        'root': [
            (r'[0-9a-f]', Number),
            (r'[+*/%!`-]', Operator),             # Traditional math
            (r'[<>^v?\[\]rxjk]', Name.Variable),  # Move, imperatives
            (r'[:\\$.,n]', Name.Builtin),         # Stack ops, imperatives
            (r'[|_mw]', Keyword),
            (r'[{}]', Name.Tag),                  # Befunge-98 stack ops
            (r'".*?"', String.Double),            # Strings don't appear to allow escapes
            (r'\'.', String.Single),              # Single character
            (r'[#;]', Comment),                   # Trampoline... depends on direction hit
            (r'[pg&~=@iotsy]', Keyword),          # Misc
            (r'[()A-Z]', Comment),                # Fingerprints
            (r'\s+', Text),                       # Whitespace doesn't matter
        ],
    }


class CAmkESLexer(RegexLexer):
    """
    Basic lexer for the input language for the
    `CAmkES <https://sel4.systems/CAmkES/>`_ component platform.

    .. versionadded:: 2.1
    """
    name = 'CAmkES'
    aliases = ['camkes', 'idl4']
    filenames = ['*.camkes', '*.idl4']

    tokens = {
        'root': [
            # C pre-processor directive
            (r'^\s*#.*\n', Comment.Preproc),

            # Whitespace, comments
            (r'\s+', Text),
            (r'/\*(.|\n)*?\*/', Comment),
            (r'//.*\n', Comment),

            (r'[\[(){},.;\]]', Punctuation),
            (r'[~!%^&*+=|?:<>/-]', Operator),

            (words(('assembly', 'attribute', 'component', 'composition',
                    'configuration', 'connection', 'connector', 'consumes',
                    'control', 'dataport', 'Dataport', 'Dataports', 'emits',
                    'event', 'Event', 'Events', 'export', 'from', 'group',
                    'hardware', 'has', 'interface', 'Interface', 'maybe',
                    'procedure', 'Procedure', 'Procedures', 'provides',
                    'template', 'thread', 'threads', 'to', 'uses', 'with'),
                   suffix=r'\b'), Keyword),

            (words(('bool', 'boolean', 'Buf', 'char', 'character', 'double',
                    'float', 'in', 'inout', 'int', 'int16_6', 'int32_t',
                    'int64_t', 'int8_t', 'integer', 'mutex', 'out', 'real',
                    'refin', 'semaphore', 'signed', 'string', 'struct',
                    'uint16_t', 'uint32_t', 'uint64_t', 'uint8_t', 'uintptr_t',
                    'unsigned', 'void'),
                   suffix=r'\b'), Keyword.Type),

            # Recognised attributes
            (r'[a-zA-Z_]\w*_(priority|domain|buffer)', Keyword.Reserved),
            (words(('dma_pool', 'from_access', 'to_access'), suffix=r'\b'),
                Keyword.Reserved),

            # CAmkES-level include
            (r'import\s+(<[^>]*>|"[^"]*");', Comment.Preproc),

            # C-level include
            (r'include\s+(<[^>]*>|"[^"]*");', Comment.Preproc),

            # Literals
            (r'0[xX][\da-fA-F]+', Number.Hex),
            (r'-?[\d]+', Number),
            (r'-?[\d]+\.[\d]+', Number.Float),
            (r'"[^"]*"', String),
            (r'[Tt]rue|[Ff]alse', Name.Builtin),

            # Identifiers
            (r'[a-zA-Z_]\w*', Name),
        ],
    }


class RedcodeLexer(RegexLexer):
    """
    A simple Redcode lexer based on ICWS'94.
    Contributed by Adam Blinkinsop <blinks@acm.org>.

    .. versionadded:: 0.8
    """
    name = 'Redcode'
    aliases = ['redcode']
    filenames = ['*.cw']

    opcodes = ('DAT', 'MOV', 'ADD', 'SUB', 'MUL', 'DIV', 'MOD',
               'JMP', 'JMZ', 'JMN', 'DJN', 'CMP', 'SLT', 'SPL',
               'ORG', 'EQU', 'END')
    modifiers = ('A', 'B', 'AB', 'BA', 'F', 'X', 'I')

    tokens = {
        'root': [
            # Whitespace:
            (r'\s+', Text),
            (r';.*$', Comment.Single),
            # Lexemes:
            #  Identifiers
            (r'\b(%s)\b' % '|'.join(opcodes), Name.Function),
            (r'\b(%s)\b' % '|'.join(modifiers), Name.Decorator),
            (r'[A-Za-z_]\w+', Name),
            #  Operators
            (r'[-+*/%]', Operator),
            (r'[#$@<>]', Operator),  # mode
            (r'[.,]', Punctuation),  # mode
            #  Numbers
            (r'[-+]?\d+', Number.Integer),
        ],
    }
