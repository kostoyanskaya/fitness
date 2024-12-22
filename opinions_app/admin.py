from flask_admin import Admin, BaseView, AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from opinions_app import app, db

from .models import ExerciseType, DayOfWeek, Coach
from .forms import ExerciseTypeForm

class DashboardView(AdminIndexView): 
    @expose('/') 
    def index(self): 
        return self.render('admin/dashboard_index.html')

class CustomExerciseTypeView(ModelView):
    form_base_class = ExerciseTypeForm
    form_columns = ('name',)

    def create_form(self):
        form = super().create_form()
        return form

admin = Admin(app, template_mode='bootstrap3', index_view=DashboardView())


admin.add_view(CustomExerciseTypeView(ExerciseType, db.session, name='Exercise Types'))
admin.add_view(ModelView(DayOfWeek, db.session, name='Days of Week'))
admin.add_view(ModelView(Coach, db.session, name='Coaches'))