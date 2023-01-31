from collections import UserDict
from datetime import datetime


from database.db import conn_to_db
from database.models import DBPerson, DBNote

from features.addressbook_fields import Record
from features.notebook_fields import NoteRecord


DATE_FORMAT = "%d.%m.%Y"


class RecordsContainer(UserDict):
    """
    A class that holds records.
    """

    def __init__(self, save_file):
        super().__init__()
        self.data = RecordsContainer.load_data(save_file) or {}

    @classmethod
    def load_data(cls, filepath: str) -> None | dict:
        """
        Loads records from a database.

        """
        conn_to_db()
        loaded_data = {}
        match filepath:
            case 'address_book.bin':
                try:
                    persons = DBPerson.objects()
                    for person_ in persons:
                        record = Record(person_.name)
                        record.name = person_.name
                        record.birthday = person_.birthday.strftime(DATE_FORMAT)
                        record.address = person_.address
                        record.email = person_.email
                        record.phones = person_.phones
                        loaded_data[person_.name] = record
                    return loaded_data
                except ConnectionError as e:
                    print(f'Unfortunately, {e}')
            case 'notebook.bin':
                try:
                    notes = DBNote.objects()
                    for note_ in notes:
                        note_record = NoteRecord(note_.title)
                        note_record.name = note_.title
                        note_record.text = note_.text
                        note_record.created = note_.created.date()
                        note_record.note_tags = {i + 1: note_.tags[i] for i in range(0, len(note_.tags), 1)}
                        loaded_data[note_.title] = note_record
                    return loaded_data
                except ConnectionError as e:
                    print(f'Unfortunately, {e}')

    @staticmethod
    def backup_data(handler) -> None:
        """
        Saves records to a database.

        :param handler: whose data to save
        """
        match handler.name():
            case 'contacts':
                DBPerson.objects.delete()
                for rec_id, record in enumerate(handler.data.values(), start=1):
                    DBPerson(
                        name=record.name,
                        birthday=datetime.strptime(record.birthday, DATE_FORMAT),
                        email=record.email,
                        address=record.address,
                        phones=record.phones).save()
            case 'notes':
                DBNote.objects.delete()
                for note_record in handler.data.values():
                    DBNote(
                        title=note_record.name,
                        text=note_record.text,
                        created=note_record.created,
                        tags=list(note_record.note_tags.values())
                    ).save()

    def add_record(self, record) -> None:
        """
        Adds a new record.

        :param record:
        :return:
        """
        self.data[record.name] = record

    def remove_record(self, *args: str) -> str:
        """
        Removes a given record. Throws exception if the record does not exist.

        :return: success message
        """

        record_name = " ".join(args)
        if self.record_exists(record_name):
            del self.data[record_name]
            return f"{record_name} was deleted successfully!"
        else:
            raise KeyError(f"{record_name} was not found!")

    def record_exists(self, record_name: str) -> bool:
        """
        Checks if record exists.

        :param record_name: a name of a record
        :return: True is exists False otherwise
        """

        return record_name in self.data

    def show_all(self) -> str:
        """
        Shows all existing records.

        :return: all records as a string
        """

        if self.data:
            result = ""
            for record in self.data.values():
                result += "\n" + str(record) + "\n"
            return result
        else:
            return "You don't have any data yet."

    def search_record(self, needle: str) -> str:
        """
        Searches and returns a record that contains a needle.

        :param needle: what to search
        :return: a result string
        """
        result = list(filter(lambda record: needle in str(record).lower(), self.data.values()))
        if result:
            return "\n".join(["\n" + str(r) for r in result])
        else:
            return "Sorry, couldn't find any records that match the query."
