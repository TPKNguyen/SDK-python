# coding: utf-8

import json
import requests

from ..utils import Utils

from ...errors import RecastError

class Message():
  def __init__(self, request, token):
    self.token = token

    request = json.loads(request)
    for k, v in request.items():
      setattr(self, k, v)

    self.conversation_id = request['message']['conversation']
    self.content = request['message']['attachment']['content']
    self.type = request['message']['attachment']['type']

    self.replies = []

  def add_replies(self, replies):
    if type(replies) is str or type(replies) is bytes:
      replies = [replies]

    self.replies = self.replies + replies

  def reply(self, replies=[]):
    if type(replies) is str or type(replies) is bytes:
      replies = [replies]

    response = requests.post(
      Utils.CONVERSATION_ENDPOINT + self.conversation_id + '/messages',
      json={'messages': self.replies + replies},
      headers={'Authorization': "Token {}".format(self.token)}
    )
    if response.status_code != requests.codes.created:
      raise RecastError(response.json()['message'])

    return response
