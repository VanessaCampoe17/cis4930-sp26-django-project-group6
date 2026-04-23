import csv
import os
from django.core.management.base import BaseCommand
from django.conf import settings
from myapp.models import SecurityEvent, AttackCategory

class Command(BaseCommand):
    help = 'Seeds the database with Cybersecurity Attack dat from Project 1'

    def handle(self, *args, **options):
        # define path to CSV'
        csv_file_path = os.path.join(settings.BASE_DIR,'data','raw','cybersecurity_attacks.csv')

        self.stdout.write(f"Loading data from: {csv_file_path}")

        try:
            with open(csv_file_path, 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    #handle ForeignKey parent - ensure category exsists before linking an event
                    category_obj, _ = AttackCategory.objects.get_or_create(
                        name=row['Attack Type'] #needs to match csv column name 
                    )

                    #requirement: use get_or_create to avoid duplicates
                    SecurityEvent.objects.get_or_create(
                        category=category_obj,
                        timestamp = row['Timestamp'], #change to match csv
                        defaults = {
                            'severity' : row['Severity Level'].lower(),
                            'threat_score':float(row['Anomaly Scores']),
                            'packet_length':float(row.get('Packet Length',0.0)),
                            'action_taken':row.get('Action Taken', 'logged').lower(),
                            'source':'csv'
                        }
                    )
            self.stdout.write(self.style.SUCCESS('Successfully seeded cybersecurity data.'))
        except FileNotFoundError:
            self.stderr.write(f"File notfound at {csv_file_path}")
        except Exception as e:
            self.stderr.write(f"An error occured: {e}")