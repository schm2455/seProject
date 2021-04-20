from abc import ABC


#User abstract class, includes basic info and methods that will be used by all users
class User(ABC):
    def __init__(self, idnumber,fname, lname, address, phone):
        self.idnumber = idnumber
        self.fname = fname
        self.lname = lname
        self.address = address
        self.phone = phone

    def get_idnumber(self):
        return self.idnumber

    def get_fname(self):
        return self.fname

    def set_fname(self, fname):
        self.fname = fname

    def get_lname(self):
        return self.lname

    def set_lname(self,lname):
        self.lname = lname

    def get_address(self):
        return self.address

    def set_address(self,address):
        self.address = address

    def get_phone(self):
        return self.phone

    def set_phone(self, phone):
        self.phone = phone


class Admin(User):
    def create_course(self):
        pass

    def create_account(self):
        pass

    def delete_account(self):
        pass

    def edit_account(self):
        pass

    def send_notification(self):
        pass

    def access_data(self):
        pass

    def assign_instructors(self):
        pass

    def assign_TAtoCourse(self):
        pass

    def assign_TAtoLab(self):
        pass

