#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sarmata.sarmata_client import validate_recognition_settings, create_audio_stream, print_results, print_results_numbers
from sarmata.service.sarmata_settings import SarmataSettings
from sarmata.service.sarmata_recognize import SarmataRecognizer
from address_provider import AddressProvider
from os.path import join as opjoin
import sys
from VoiceRecording import VoiceRecording
from run_trybun import *
from run_dictation import *



class SarmataArgs:
    address = None                      # IP address and port (address:port) of a service the client will connect to.
    define_grammar = False              # Defines a new grammar to be cached by the service under ID given by `--grammar-name` option from data given by `--grammar` option.
    grammar_name = ''                   # Name (ID) of the grammar in the service's grammar cache.
    grammar = None                      # SRGS grammar file (ABNF or XML format accepted).
    max_alternatives = 3                # Maximum number of recognition hypotheses to be returned.
    mic = False                         # Use microphone as an audio source (instead of wave file).
    no_input_timeout = 5000             # MRCP v2 no input timeout [ms].
    no_match_threshold = 0.2            # Confidence acceptance threshold.
    recognition_timeout = 10000        # MRCP v2 recognition timeout [ms].
    session_id = None                   # Session ID to be passed to the service. If not specified, the service will generate a default session ID itself.
    service_settings = None             # Semicolon-separated list of key=value pairs defining settings to be sent to service via gRPC request.
    speech_complete_timeout = 5000      # MRCP v2 speech complete timeout [ms].
    speech_incomplete_timeout = 3000    # MRCP v2 speech incomplete timeout [ms].
    wave = None                         # Path to wave file with speech to be recognized. Should be mono, 8kHz or 16kHz.


    def __init__(self, wav_filepath=None, grammar=None):
        ap = AddressProvider()
        if grammar:
            self.grammar = grammar
        if wav_filepath:
            self.wave = opjoin(wav_filepath)
        self.address = ap.get("sarmata")

class SarmataVoiceRecognition:
    def menu_choice_recognition(self, grammar_file):
        vr = VoiceRecording()
        vr.record_voice()

        wave_file = "waves/output6.wav"
        args = SarmataArgs(wave_file, grammar_file)

        settings = SarmataSettings()
        settings.process_args(args)  # load settings from cmd
        if args.grammar is not None:
            settings.load_grammar(args.grammar)

        can_define_grammar = False
        if args.define_grammar:
            if not settings.grammar_name:
                print("Bad usage. Set BOTH grammar_name and grammar file when define grammar is set True.")
                sys.exit(1)
            can_define_grammar = True

        recognizer = SarmataRecognizer(args.address)

        if can_define_grammar:
            define_grammar_response = recognizer.define_grammar(args.grammar_name, settings.grammar)
            if define_grammar_response.ok:
                if args.grammar is None:
                    print("Grammar " + args.grammar_name + " removed")
                else:
                    print("Grammar " + args.grammar + " defined as " + args.grammar_name)
            else:
                print("Define grammar error: " + define_grammar_response.error)

        # --------------------------
        # recognize section
        # --------------------------
        if args.wave is not None or args.mic:
            validate_recognition_settings(settings)

            try:
                with create_audio_stream(args) as stream:
                    # generate id
                    session_id = stream.session_id()
                    settings.set_session_id(session_id)

                    results = recognizer.recognize(stream, settings)
                    res_semantic_interpretation = print_results(results, stream)

                    if res_semantic_interpretation == None:
                        raise Exception

                    else:
                        print(res_semantic_interpretation)
                        # zwraca interpretacje
                        return res_semantic_interpretation
            except Exception:
                print("Bład")
                return -1

class SarmataVoiceRecognitionNumbers:
    def menu_choice_recognition(self, grammar_file):
        vr = VoiceRecording()
        vr.record_voice()

        wave_file = "waves/output6.wav"
        args = SarmataArgs(wave_file, grammar_file)

        settings = SarmataSettings()
        settings.process_args(args)  # load settings from cmd
        if args.grammar is not None:
            settings.load_grammar(args.grammar)

        can_define_grammar = False
        if args.define_grammar:
            if not settings.grammar_name:
                print("Bad usage. Set BOTH grammar_name and grammar file when define grammar is set True.")
                sys.exit(1)
            can_define_grammar = True

        recognizer = SarmataRecognizer(args.address)

        if can_define_grammar:
            define_grammar_response = recognizer.define_grammar(args.grammar_name, settings.grammar)
            if define_grammar_response.ok:
                if args.grammar is None:
                    print("Grammar " + args.grammar_name + " removed")
                else:
                    print("Grammar " + args.grammar + " defined as " + args.grammar_name)
            else:
                print("Define grammar error: " + define_grammar_response.error)

        # --------------------------
        # recognize section
        # --------------------------
        if args.wave is not None or args.mic:
            validate_recognition_settings(settings)

            try:
                with create_audio_stream(args) as stream:
                    # generate id
                    session_id = stream.session_id()
                    settings.set_session_id(session_id)

                    results = recognizer.recognize(stream, settings)
                    rec_number_transcription = print_results_numbers(results, stream)
                    if rec_number_transcription == None:
                        raise Exception
                    else:
                        print(rec_number_transcription)
                        trybun = Trybun()
                        trybun.text_to_wave(rec_number_transcription + ". Liczba.")
                        dictation = Dictation()
                        recognized_number = dictation.dictation_recognize_numbers()
                        print(recognized_number)
                        return recognized_number
            except Exception:
                return -1


if __name__ == '__main__':
    vr = VoiceRecording()
    vr.record_voice()

    wave_file = "waves/output6.wav"
    grammar_file = "grammars/menu.abnf"
    args = SarmataArgs(wave_file, grammar_file)

    settings = SarmataSettings()
    settings.process_args(args)  # load settings from cmd
    if args.grammar is not None:
        settings.load_grammar(args.grammar)

    can_define_grammar = False
    if args.define_grammar:
        if not settings.grammar_name:
            print("Bad usage. Set BOTH grammar_name and grammar file when define grammar is set True.")
            sys.exit(1)
        can_define_grammar = True

    recognizer = SarmataRecognizer(args.address)

    if can_define_grammar:
        define_grammar_response = recognizer.define_grammar(args.grammar_name, settings.grammar)
        if define_grammar_response.ok:
            if args.grammar is None:
                print("Grammar " + args.grammar_name + " removed")
            else:
                print("Grammar " + args.grammar + " defined as " + args.grammar_name)
        else:
            print("Define grammar error: " + define_grammar_response.error)

    # --------------------------
    # recognize section
    # --------------------------
    if args.wave is not None or args.mic:
        validate_recognition_settings(settings)

        with create_audio_stream(args) as stream:
            # generate id
            session_id = stream.session_id()
            settings.set_session_id(session_id)

            results = recognizer.recognize(stream, settings)
            res_semantic_interpretation = print_results(results, stream)

            print(res_semantic_interpretation)