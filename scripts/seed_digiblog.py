"""
Seed script for digiblog app - Creates 1000+ blog posts with comments
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
from apps.digiblog.models import BlogPost, Comment, BlogLike, BlogFollow
from apps.accounts.models import User

fake = Faker()
Faker.seed(42)

def create_blog_posts(count=1000):
    """Create blog posts"""
    print(f"\n📝 Creating {count} blog posts...")
    
    authors = list(User.objects.filter(role='mentor').all())[:100]
    if not authors:
        authors = list(User.objects.all())[:100]
    
    if not authors:
        print("⚠️  No authors found")
        return []
    
    categories = ['study_hacks', 'mental_health', 'scholarships', 'cbc_updates', 'tech', 'career_guidance']
    statuses = ['draft', 'published', 'archived']
    
    posts = []
    for i in range(count):
        post = BlogPost.objects.create(
            title=f"{fake.sentence(nb_words=6)} - Blog {i:04d}",
            author=fake.random_element(authors),
            category=fake.random_element(categories),
            content=fake.paragraph(nb_sentences=20),
            excerpt=fake.sentence(),
            status=fake.random_element(statuses),
            is_featured=fake.boolean(chance_percent=10),
            views_count=fake.random_int(min=0, max=5000),
            likes_count=fake.random_int(min=0, max=500),
            comments_count=fake.random_int(min=0, max=100),
            meta_description=fake.sentence(),
            tags=", ".join([fake.word() for _ in range(3)]),
            published_at=timezone.now() - timedelta(days=fake.random_int(min=1, max=365))
            if fake.boolean(chance_percent=80) else None
        )
        posts.append(post)
        
        if (i + 1) % 100 == 0:
            print(f"  ✓ Created {i + 1} posts")
    
    print(f"✅ Created {count} blog posts")
    return posts

def create_comments(posts):
    """Create comments on blog posts"""
    print(f"\n💬 Creating comments on blog posts...")
    
    users = list(User.objects.all())[:500]
    if not users:
        print("⚠️  No users found")
        return []
    
    comments = []
    comment_count = 0
    
    for post in posts:
        # Create 1-10 comments per post
        num_comments = fake.random_int(min=1, max=10)
        for _ in range(num_comments):
            comment = Comment.objects.create(
                post=post,
                author=fake.random_element(users),
                content=fake.paragraph(nb_sentences=3),
                is_approved=fake.boolean(chance_percent=95),
                is_flagged=fake.boolean(chance_percent=5)
            )
            comments.append(comment)
            comment_count += 1
        
        if comment_count % 500 == 0:
            print(f"  ✓ Created {comment_count} comments")
    
    print(f"✅ Created {comment_count} comments total")
    return comments

def create_blog_likes(posts):
    """Create likes on blog posts"""
    print(f"\n👍 Creating blog likes...")
    
    users = list(User.objects.all())[:1000]
    if not users:
        print("⚠️  No users found")
        return []
    
    likes = []
    like_count = 0
    
    for post in posts:
        # Each post gets 5-100 likes
        num_likes = fake.random_int(min=5, max=100)
        available_users = users.copy()
        
        for _ in range(min(num_likes, len(available_users))):
            user = available_users.pop()
            try:
                like = BlogLike.objects.create(
                    post=post,
                    user=user
                )
                likes.append(like)
                like_count += 1
            except:
                pass  # Unique constraint violation
        
        if like_count % 500 == 0:
            print(f"  ✓ Created {like_count} likes")
    
    print(f"✅ Created {like_count} likes total")
    return likes

def create_blog_follows():
    """Create blog author follows"""
    print(f"\n🔗 Creating blog follows...")
    
    users = list(User.objects.all())
    if len(users) < 2:
        print("⚠️  Not enough users")
        return []
    
    follows = []
    follow_count = 0
    
    for follower in users[:500]:
        # Each user follows 5-20 other users
        num_follows = fake.random_int(min=5, max=20)
        available_users = [u for u in users if u.id != follower.id]
        
        for _ in range(min(num_follows, len(available_users))):
            following = fake.random_element(available_users)
            try:
                follow = BlogFollow.objects.create(
                    follower=follower,
                    following=following
                )
                follows.append(follow)
                follow_count += 1
            except:
                pass  # Unique constraint violation
        
        if follow_count % 500 == 0:
            print(f"  ✓ Created {follow_count} follows")
    
    print(f"✅ Created {follow_count} follows total")
    return follows

def main():
    """Main seeding function"""
    print("=" * 60)
    print("🌱 DIGIBLOG APP SEEDING")
    print("=" * 60)
    
    try:
        posts = create_blog_posts(count=1000)
        comments = create_comments(posts)
        likes = create_blog_likes(posts)
        follows = create_blog_follows()
        
        print("\n" + "=" * 60)
        print(f"✅ SUCCESS: DigiBlob app seeded")
        print(f"   - {len(posts)} blog posts")
        print(f"   - {len(comments)} comments")
        print(f"   - {len(likes)} likes")
        print(f"   - {len(follows)} follows")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
