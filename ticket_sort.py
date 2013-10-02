#!/usr/bin/env python
import json

class Ticket(object):

    def __init__(self, from_dir, to_dir, transport_name, additional_info=''):
        self.from_dir = from_dir
        self.to_dir = to_dir
        self.next = None
        self.transport_name = transport_name
        self.info = additional_info

    def get_info(self):
        return 'Take {transport_name} from {from_dir} to {to_dir}.{info}'.format(**self.__dict__)

class TicketSort(object):

    direction_dict = {}
    sorted_tickets = []
    first_ticket = None
    tickets_num = 0

    def __init__(self, tickets_data, format='json'):
        """ Input - tickets data in format 
            [
                {   'from_dir': str, 
                    'to_dir': str, 
                    'transport_name': str, 
                    'additional_info': str},
                 ....
                {.....}
            ]

            Output - streamming info (string) for each sorted ticket 
        """
        formst = format.lower()
        if format == 'json':
            tickets = json.loads(tickets_data)
            # TODO Validation schema (for example jsonschema)
            valid_schema = True

        elif format == 'xml':
            # TODO XML validate and serialize
            pass
        else:
            # TODO error message
            raise

        if valid_schema:
            self.tickets_num = len(tickets)
            for t in tickets:
                ticket = Ticket(**t)
                next_ticket = self.direction_dict.get(t['to_dir'], None)
                prev_ticket = self.direction_dict.get(t['from_dir'], None)

                if next_ticket:
                    ticket.next = next_ticket
                    del self.direction_dict[t['to_dir']]
                else:
                    self.direction_dict[t['to_dir']] = ticket

                if prev_ticket:
                    prev_ticket.next = ticket
                    del self.direction_dict[t['from_dir']]
                else:
                    self.direction_dict[t['from_dir']] = ticket

            self.first_ticket = filter(lambda x: x.next, self.direction_dict.values())[0]
            self.direction_dict.clear()

    def sort_tickets(self):
        n = 1
        t = self.first_ticket
        yield t
        while n < self.tickets_num:
            t = t.next
            n += 1
            yield t.get_info()

def test(n):
    tickets_data=[]
    for i in xrange(1,n):
        if i%2:
            tickets_data.append({'from_dir': str(i)+'from', 'to_dir': str(i+1)+'to', 'transport_name': 'bus'})
        else:
            tickets_data.append({'from_dir': str(i)+'to', 'to_dir': str(i+1)+'from', 'transport_name': 'train', 
                'additional_info': 'Seat{}A'.format(str(i))
                })

    from random import shuffle
    shuffle(tickets_data)

    tks = TicketSort(json.dumps(tickets_data))
    for t in tks.sort_tickets():
        print t


# Usage example
if __name__ == '__main__':
    test(100000)