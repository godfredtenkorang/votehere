# management/commands/upload_voters.py
import json
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from models import Election, Voter

class Command(BaseCommand):
    help = 'Upload voters from JSON file to a specific election'
    
    def add_arguments(self, parser):
        parser.add_argument('election_id', type=int, help='ID of the election')
        parser.add_argument('json_file', type=str, help='Path to JSON file')
        parser.add_argument(
            '--default-password',
            type=str,
            help='Default password to use if not specified in JSON',
            default='default123'
        )
        parser.add_argument(
            '--use-custom-passwords',
            action='store_true',
            help='Use passwords from JSON file (required password field in JSON)'
        )
    
    def handle(self, *args, **options):
        election_id = options['election_id']
        json_file_path = options['json_file']
        default_password = options['default_password']
        use_custom_passwords = options['use_custom_passwords']
        
        try:
            election = Election.objects.get(id=election_id)
        except Election.DoesNotExist:
            self.stderr.write(f"Election with ID {election_id} does not exist")
            return
        
        try:
            with open(json_file_path, 'r') as file:
                voter_data = json.load(file)
        except FileNotFoundError:
            self.stderr.write(f"File {json_file_path} not found")
            return
        except json.JSONDecodeError:
            self.stderr.write("Invalid JSON file")
            return
        
        success_count = 0
        error_count = 0
        
        for voter_info in voter_data:
            try:
                username = voter_info.get('username')
                email = voter_info.get('email')
                unique_key = voter_info.get('unique_key')
                custom_password = voter_info.get('password')
                
                if not all([username, email, unique_key]):
                    self.stdout.write(f"Missing required fields for voter: {voter_info}")
                    error_count += 1
                    continue
                
                # Password handling
                if use_custom_passwords:
                    if not custom_password:
                        self.stdout.write(f"Custom password required but not provided for: {username}")
                        error_count += 1
                        continue
                    password = custom_password
                else:
                    password = default_password
                
                if Voter.objects.filter(unique_key=unique_key).exists():
                    self.stdout.write(f"Voter with unique key '{unique_key}' already exists")
                    error_count += 1
                    continue
                
                # Create or update user
                if User.objects.filter(username=username).exists():
                    user = User.objects.get(username=username)
                    user.email = email
                    user.set_password(password)
                    user.save()
                else:
                    user = User.objects.create_user(
                        username=username,
                        email=email,
                        password=password
                    )
                
                # Create voter
                Voter.objects.create(
                    election=election,
                    user=user,
                    unique_key=unique_key
                )
                
                success_count += 1
                self.stdout.write(f"Created voter: {username}")
                
            except Exception as e:
                self.stdout.write(f"Error creating voter {voter_info}: {str(e)}")
                error_count += 1
        
        self.stdout.write(
            self.style.SUCCESS(
                f"Upload complete: {success_count} successful, {error_count} errors"
            )
        )