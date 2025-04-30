from django.db import models

class members(models.Model):
    member_id=models.CharField(max_length=10, primary_key=True)
    member_name=models.CharField(max_length=100)
    member_address=models.CharField(max_length=100)
    reg_date = models.DateField()
    
    def __str__(self):
        return self.member_name


class books(models.Model):
    isbn=models.CharField(max_length=13)
    title=models.CharField(max_length=200)
    author=models.CharField(max_length=200)
    category=models.CharField(max_length=100)
    rental_price = models.DecimalField(max_digits=5, decimal_places=2)
    status = models.BooleanField(default=True)
    publisher = models.CharField(max_length=200)
    
    def __str__(self):
        return self.title
    
class branch(models.Model):
    branch_id=models.CharField(max_length=10, primary_key=True)
    manager_id=models.CharField(max_length=10)
    branch_address=models.CharField(max_length=100)
    contact_no=models.CharField(max_length=15)
    
    def _str_(self):
        return self.branch_id
    
class employees(models.Model):
    emp_id = models.CharField(max_length=10, primary_key=True)
    emp_name = models.CharField(max_length=100)
    position = models.CharField(max_length=50)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    branch = models.ForeignKey(branch, on_delete=models.CASCADE)

    def __str__(self):
        return self.emp_name
    
    
class issued_status(models.Model):
    issued_id = models.CharField(max_length=10, primary_key=True)
    issued_member = models.ForeignKey(members, on_delete=models.CASCADE)
    issued_book_name = models.CharField(max_length=200)
    issued_date = models.DateField()
    issued_book = models.ForeignKey(books, on_delete=models.CASCADE)
    issued_emp = models.ForeignKey(employees, on_delete=models.CASCADE)

    def __str__(self):
        return self.issued_id  
class return_status(models.Model):
    return_id = models.CharField(max_length=10, primary_key=True)
    issued = models.ForeignKey(issued_status, on_delete=models.CASCADE)
    return_date = models.DateField()

    def __str__(self):
        return self.return_id
