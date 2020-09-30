# -*- coding: utf-8 -*-

import logging
import ask_sdk_core.utils as ask_utils

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model.ui import SimpleCard
from ask_sdk_model.ui import StandardCard
from ask_sdk_model.ui.image import Image

from ask_sdk_model import Response

from datetime import date, timedelta
import requests
import json

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


chave_sistema = "XXXX"
codEmpresa = "XXXXX"
codApp = "XXXXX"

url_base = "https://app.staging.dotbank.com.br/api/v1/"


imagem_padrao = Image("https://i.imgur.com/VxXfaz3.jpg", "https://i.imgur.com/VxXfaz3.jpg")

'''
    Alexa vai poder interagir com o usuario de forma complexa por meio de estados.
    
=== ESTADOS ===
    
Estado 0 = Estado Inicial.
Estado 100 = Estado de confirmacao de cadastro de pessoa.
Estado 200 = Estado de confirmacao de cadastro de produto.
Estado 300 = Estado de conformacao de cobranca
'''

#=========INTENTS============================================================
#Ponto de entrada
class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool

        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        
        speak_output = "Bem vindo ao Dóti Benk. Como posso te ajudar?"
        
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


#=== Classes Personalizadas ===
from cadastro_de_pessoas import cadastrarPessoaIntentHandler, cadastrarPessoaJuridicaIntentHandler


from faturas import faturasHandler

from pagamentos import pagamentoHojeHandler
from pagamentos import pagamentoNoPeriodoHandler

from sim_e_nao import NoIntentHandler
from sim_e_nao import YesIntentHandler

from valor_produto import custoProdutoIntentHandler

from cobranca import cobrancaIntentHandler
from cobranca import meioIntentHandler


#=== Classes Padrao===
from classes_padrao import HelpIntentHandler
from classes_padrao import IntentReflectorHandler
from classes_padrao import SessionEndedRequestHandler
from classes_padrao import CancelOrStopIntentHandler
from classes_padrao import CatchAllExceptionHandler


#============SkillBuilder==================================================

sb = SkillBuilder()

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(YesIntentHandler())
sb.add_request_handler(NoIntentHandler())
sb.add_request_handler(custoProdutoIntentHandler())
sb.add_request_handler(cadastrarPessoaIntentHandler())
sb.add_request_handler(cadastrarPessoaJuridicaIntentHandler())
sb.add_request_handler(faturasHandler())
sb.add_request_handler(pagamentoHojeHandler())
sb.add_request_handler(pagamentoNoPeriodoHandler())
sb.add_request_handler(cobrancaIntentHandler())
sb.add_request_handler(meioIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(IntentReflectorHandler()) # Precisa ser por ultimo para nao sobreescrever os outros handlers

sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()
