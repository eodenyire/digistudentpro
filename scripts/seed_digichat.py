"""
Seed script for digichat app - Creates squads and 1000+ messages
"""
import os
import sys
import django
from datetime import timedelta

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
django.setup()

from django.utils import timezone
from faker import Faker
from apps.digichat.models import Squad, SquadMembership, Message, DirectMessage
from apps.accounts.models import User

fake = Faker()
Faker.seed(42)

def create_squads(count=100):
    """Create squad groups"""
    print(f"\n👥 Creating {count} squads...")
    
    users = list(User.objects.all())[:500]
    topics = [
        'Mathematics', 'Science', 'Technology', 'Business', 'Arts',
        'Sports', 'Music', 'Debate', 'Coding', 'Entrepreneurship',
        'Environment', 'Health', 'Writing', 'Design', 'Marketing'
    ]
    
    squads = []
    for i in range(count):
        squad = Squad.objects.create(
            name=f"{fake.random_element(topics)} Squad {i:03d}",
            description=fake.paragraph(nb_sentences=3),
            topic=fake.random_element(topics),
            created_by=fake.random_element(users),
            is_public=fake.boolean(chance_percent=80),
            max_members=fake.random_int(min=20, max=200)
        )
        squads.append(squad)
        
        if (i + 1) % 10 == 0:
            print(f"  ✓ Created {i + 1} squads")
    
    print(f"✅ Created {count} squads")
    return squads

def create_squad_memberships(squads):
    """Add members to squads"""
    print(f"\n📋 Creating squad memberships...")
    
    users = list(User.objects.all())
    roles = ['admin', 'moderator', 'member']
    
    memberships = []
    membership_count = 0
    
    for squad in squads:
        # Add 10-100 members to each squad
        num_members = fake.random_int(min=10, max=100)
        available_users = users.copy()
        
        for _ in range(min(num_members, len(available_users))):
            user = available_users.pop()
            try:
                membership = SquadMembership.objects.create(
                    squad=squad,
                    user=user,
                    role=fake.random_element(roles)
                )
                memberships.append(membership)
                membership_count += 1
            except:
                pass  # Unique constraint
        
        if membership_count % 500 == 0:
            print(f"  ✓ Created {membership_count} memberships")
    
    print(f"✅ Created {membership_count} memberships")
    return memberships

def create_squad_messages(squads):
    """Create messages in squads"""
    print(f"\n💬 Creating squad messages...")
    
    users = list(User.objects.all())
    messages = []
    message_count = 0
    
    for squad in squads:
        # Get squad members
        members = squad.members.all()
        if not members.exists():
            continue
        
        # Create 5-30 messages per squad
        num_messages = fake.random_int(min=5, max=30)
        for _ in range(num_messages):
            try:
                message = Message.objects.create(
                    squad=squad,
                    sender=fake.random_element(list(members)),
                    content=fake.sentence(),
                    is_flagged=fake.boolean(chance_percent=2)
                )
                messages.append(message)
                message_count += 1
            except:
                pass
        
        if message_count % 500 == 0:
            print(f"  ✓ Created {message_count} messages")
    
    print(f"✅ Created {message_count} squad messages")
    return messages

def create_direct_messages():
    """Create direct messages between users"""
    print(f"\n💌 Creating direct messages...")
    
    users = list(User.objects.all())
    if len(users) < 2:
        print("⚠️  Not enough users")
        return []
    
    messages = []
    message_count = 0
    
    # Create 1000 direct messages
    for _ in range(1000):
        sender, recipient = fake.random_elements(elements=users, length=2, unique=True)
        try:
            message = DirectMessage.objects.create(
                sender=sender,
                recipient=recipient,
                content=fake.sentence(),
                is_read=fake.boolean(),
                read_at=timezone.now() if fake.boolean() else None,
                is_flagged=fake.boolean(chance_percent=2)
            )
            messages.append(message)
            message_count += 1
        except:
            pass
        
        if message_count % 100 == 0:
            print(f"  ✓ Created {message_count} direct messages")
    
    print(f"✅ Created {message_count} direct messages")
    return messages

def main():
    """Main seeding function"""
    print("=" * 60)
    print("🌱 DIGICHAT APP SEEDING")
    print("=" * 60)
    
    try:
        squads = create_squads(count=100)
        memberships = create_squad_memberships(squads)
        squad_messages = create_squad_messages(squads)
        direct_messages = create_direct_messages()
        
        print("\n" + "=" * 60)
        print(f"✅ SUCCESS: DigiChat app seeded")
        print(f"   - {len(squads)} squads")
        print(f"   - {len(memberships)} memberships")
        print(f"   - {len(squad_messages)} squad messages")
        print(f"   - {len(direct_messages)} direct messages")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
