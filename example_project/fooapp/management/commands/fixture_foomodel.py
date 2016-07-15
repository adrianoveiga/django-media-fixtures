from django.core.management.base import BaseCommand, CommandError

from fooapp.models import FooModel

# simple load/create fixture entries
class Command(BaseCommand):
    help = 'Load FooModel\'s fixtures'

    def handle(self, **options):
        self.stdout.write('Loading FooModel\'s fixtures...')
        
        # #Criando Artigos
        foomodel_1, created = FooModel.objects.get_or_create(description="Sample 1", image="uploads/foomodel/img/board.jpg")
