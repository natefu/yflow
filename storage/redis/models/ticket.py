from storage.redis.models.base import BaseModel, Field, Category, ForeignField, DatetimeField


class Ticket(BaseModel):
    name = Field(category=Category.STRING)
    state = Field(category=Category.STRING)
    variables = Field(category=Category.DICT)
    context = Field(category=Category.DICT)
    scheme = Field(category=Category.DICT)
    process = ForeignField('process')
    created = DatetimeField(auto_now_add=True)
    updated = DatetimeField(auto_now=True)
    completed = DatetimeField(auto_now=True)

    class Meta:
        index_name = 'ticket'
        unique_keys = []


class TicketToken(BaseModel):
    ticket = ForeignField('ticket')
    token = Field(category=Category.STRING)
    count = Field(category=Category.INT)
    created = DatetimeField(auto_now_add=True)
    updated = DatetimeField(auto_now=True)

    class Meta:
        index_name = 'ticket_token'
        unique_keys = [['ticket', 'token']]
