import random

from lib.database.querier import QueryResult, QueryResultCode

unknown_topic = [
    "I'm afraid I didn't quite get what you want to ask me. :(",
    "Could you maybe try rephrasing that? I don't understand what you're asking...",
    "Looks like I'm having some trouble understanding what you mean, could you try changing the question a bit?"
]

no_data_available_for_date = [
    "Sorry, I'm afraid I don't have the required data for that time period.",
    "I understand your question, but unfortunately I don't have the necessary data to answer it for you."
]

unexpected_result = [
    "It looks like I got an unexpected result when processing your question... Try notifying the adminstrator "
    "with the question you sent.",
    "That's odd, I encountered an unknown issue while finding out the answer to your question... Try notifying the "
    "adminstrator with the question you sent."
]

future_date_requested = [
    "Sorry pal, I can't look into the future. :(",
    "Ha, I do know a lot, but I cannot predict the future.",
    "Maybe you should try asking this a clairvoyant.",
    "Nice try, but I can't give you data on the future. ;)"
]

no_world_wide_supported = [
    "You need to specify the country you are want the data on.",
    "Sorry, at the moment I can't calculate statistics for the whole world and continents, "
    "only specific countries.",
    "Please specify the country you want to ask about."
]

not_existing_location = [
    "I don't have any data on {location}, try a different country. Keep in mind that I only have data on countries.",
    "Looks like I can't find any data on {location} in the database. Keep in mind that I only have data on countries."
]


class AnswerGenerator:
    def __init__(self):
        pass

    def generate_answer(self, query_result: QueryResult) -> str:
        if query_result.result_code == QueryResultCode.UNKNOWN_TOPIC:
            return random.choice(unknown_topic)
        elif query_result.result_code == QueryResultCode.NO_DATA_AVAILABLE_FOR_DATE:
            return random.choice(no_data_available_for_date)
        elif query_result.result_code == QueryResultCode.UNEXPECTED_RESULT:
            return random.choice(unexpected_result)
        elif query_result.result_code == QueryResultCode.FUTURE_DATA_REQUESTED:
            return random.choice(future_date_requested)
        elif query_result.result_code == QueryResultCode.NOT_EXISTING_LOCATION:
            return random.choice(not_existing_location).format(location=query_result.information["location"])
        else:
            print(query_result)
            raise NotImplementedError()


if __name__ == '__main__':
    pass
