import os
import pickle

class Contact:
    def __init__(self, first_name, last_name, middle_name, organization, work_phone, personal_phone):
        self.first_name = first_name
        self.last_name = last_name
        self.middle_name = middle_name
        self.organization = organization
        self.work_phone = work_phone
        self.personal_phone = personal_phone

class Phonebook:
    def __init__(self, file_name):
        self.file_name = file_name
        self.contacts = self.load_contacts()

    def load_contacts(self):
        if os.path.exists(self.file_name):
            with open(self.file_name, 'rb') as f:
                contacts = pickle.load(f)
            return contacts
        return []

    def save_contacts(self):
        with open(self.file_name, 'wb') as f:
            pickle.dump(self.contacts, f)

    def add_contact(self, contact):
        self.contacts.append(contact)
        self.save_contacts()

    def edit_contact(self, index, updated_contact):
        self.contacts[index] = updated_contact
        self.save_contacts()

    def search_contacts(self, search_terms):
        results = []
        for contact in self.contacts:
            if all(term.lower() in str(contact).lower() for term in search_terms):
                results.append(contact)
        return results

def main():
    phonebook = Phonebook('phonebook.pkl')

    while True:
        print("\n1. Вывод записей")
        print("2. Добавление записи")
        print("3. Редактирование записи")
        print("4. Поиск записей")
        print("5. Выход")
        choice = input("Выберите действие: ")

        if choice == '1':
            page = 1
            items_per_page = 5
            while True:
                start_idx = (page - 1) * items_per_page
                end_idx = start_idx + items_per_page
                for idx, contact in enumerate(phonebook.contacts[start_idx:end_idx], start=start_idx):
                    print(f"{idx + 1}. {contact.last_name} {contact.first_name} - {contact.work_phone}")
                print("\nСтраница:", page)
                print("N. Следующая страница")
                print("P. Предыдущая страница")
                print("B. Назад")
                action = input("Выберите действие: ").lower()

                if action == 'n':
                    page += 1
                elif action == 'p':
                    page = max(1, page - 1)
                elif action == 'b':
                    break

        elif choice == '2':
            first_name = input("Введите имя: ")
            last_name = input("Введите фамилию: ")
            middle_name = input("Введите отчество: ")
            organization = input("Введите название организации: ")
            work_phone = input("Введите рабочий телефон: ")
            personal_phone = input("Введите личный телефон: ")
            new_contact = Contact(first_name, last_name, middle_name, organization, work_phone, personal_phone)
            phonebook.add_contact(new_contact)
            print("Запись добавлена!")

        elif choice == '3':
            index = int(input("Введите номер записи для редактирования: ")) - 1
            if 0 <= index < len(phonebook.contacts):
                updated_contact = phonebook.contacts[index]
                print("Текущая информация:")
                print(updated_contact.__dict__)
                updated_contact.first_name = input("Введите новое имя: ")
                updated_contact.last_name = input("Введите новую фамилию: ")
                updated_contact.middle_name = input("Введите новое отчество: ")
                updated_contact.organization = input("Введите новое название организации: ")
                updated_contact.work_phone = input("Введите новый рабочий телефон: ")
                updated_contact.personal_phone = input("Введите новый личный телефон: ")
                phonebook.edit_contact(index, updated_contact)
                print("Запись обновлена!")
            else:
                print("Неверный номер записи!")

        elif choice == '4':
            search_terms = input("Введите одну или несколько характеристик для поиска (через пробел): ").split()
            search_results = phonebook.search_contacts(search_terms)
            if search_results:
                print("\nРезультаты поиска:")
                for contact in search_results:
                    print(contact.__dict__)
            else:
                print("Ничего не найдено.")

        elif choice == '5':
            break

if __name__ == "__main__":
    main()
