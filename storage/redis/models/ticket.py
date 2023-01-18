from storage.redis.models.base import BaseModel, Field, Category, ForeignField, DatetimeField
from storage.redis.models.process import Process


class Ticket(BaseModel):
    name = Field(category=Category.STRING)
    state = Field(category=Category.STRING)
    variables = Field(category=Category.DICT)
    context = Field(category=Category.DICT)
    scheme = Field(category=Category.DICT)
    process = ForeignField(Process)
    created = DatetimeField(auto_now_add=True)
    updated = DatetimeField(auto_now=True)
    completed = DatetimeField(auto_now=True)

    class Meta:
        index_name = 'ticket'
        unique_keys = []


class TicketToken(BaseModel):
    ticket = ForeignField(Ticket)
    token = Field(category=Category.STRING)
    count = Field(category=Category.INT)
    created = DatetimeField(auto_now_add=True)
    updated = DatetimeField(auto_now=True)

    class Meta:
        index_name = 'ticket_token'
        unique_keys = [['ticket', 'token']]


if __name__ == '__main__':
    #ticket = Ticket(name='ticket2', state='ready', variables={}, context={}, scheme={}, process=1)
    #print(ticket.save())
    ticket = Ticket.from_redis(14)
    print(ticket.process.value)
