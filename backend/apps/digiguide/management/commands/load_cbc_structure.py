"""
Django management command to load CBC education levels, grades, and subjects
"""
from django.core.management.base import BaseCommand
from apps.digiguide.models import EducationLevel, Grade, Subject


class Command(BaseCommand):
    help = 'Load CBC structure data (Education Levels, Grades, and Subjects)'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.NOTICE('Loading CBC structure data...'))
        
        # Load Education Levels
        self.load_education_levels()
        
        # Load Grades
        self.load_grades()
        
        # Load Subjects
        self.load_subjects()
        
        self.stdout.write(self.style.SUCCESS('Successfully loaded CBC structure data!'))

    def load_education_levels(self):
        """Load Kenya CBC Education Levels"""
        self.stdout.write('Loading Education Levels...')
        
        education_levels = [
            {
                'name': 'Pre-Primary',
                'code': 'PP',
                'description': 'Pre-Primary education level (PP1, PP2)',
                'order': 1
            },
            {
                'name': 'Lower Primary',
                'code': 'LP',
                'description': 'Lower Primary education level (Grades 1-3)',
                'order': 2
            },
            {
                'name': 'Upper Primary',
                'code': 'UP',
                'description': 'Upper Primary education level (Grades 4-6)',
                'order': 3
            },
            {
                'name': 'Junior Secondary',
                'code': 'JS',
                'description': 'Junior Secondary education level (Grades 7-9)',
                'order': 4
            },
            {
                'name': 'Senior Secondary',
                'code': 'SS',
                'description': 'Senior Secondary education level (Grades 10-12)',
                'order': 5
            },
            {
                'name': 'University',
                'code': 'UNIV',
                'description': 'University education level (Year 1-4+)',
                'order': 6
            },
        ]
        
        for level_data in education_levels:
            level, created = EducationLevel.objects.get_or_create(
                code=level_data['code'],
                defaults=level_data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'  ✓ Created: {level.name}'))
            else:
                self.stdout.write(f'  - Already exists: {level.name}')

    def load_grades(self):
        """Load Grades for each Education Level"""
        self.stdout.write('Loading Grades...')
        
        grades_data = [
            # Pre-Primary
            {'level_code': 'PP', 'name': 'PP1', 'code': 'PP1', 'order': 1, 'age_range': '4-5 years'},
            {'level_code': 'PP', 'name': 'PP2', 'code': 'PP2', 'order': 2, 'age_range': '5-6 years'},
            
            # Lower Primary
            {'level_code': 'LP', 'name': 'Grade 1', 'code': 'G1', 'order': 1, 'age_range': '6-7 years'},
            {'level_code': 'LP', 'name': 'Grade 2', 'code': 'G2', 'order': 2, 'age_range': '7-8 years'},
            {'level_code': 'LP', 'name': 'Grade 3', 'code': 'G3', 'order': 3, 'age_range': '8-9 years'},
            
            # Upper Primary
            {'level_code': 'UP', 'name': 'Grade 4', 'code': 'G4', 'order': 1, 'age_range': '9-10 years'},
            {'level_code': 'UP', 'name': 'Grade 5', 'code': 'G5', 'order': 2, 'age_range': '10-11 years'},
            {'level_code': 'UP', 'name': 'Grade 6', 'code': 'G6', 'order': 3, 'age_range': '11-12 years'},
            
            # Junior Secondary
            {'level_code': 'JS', 'name': 'Grade 7', 'code': 'G7', 'order': 1, 'age_range': '12-13 years'},
            {'level_code': 'JS', 'name': 'Grade 8', 'code': 'G8', 'order': 2, 'age_range': '13-14 years'},
            {'level_code': 'JS', 'name': 'Grade 9', 'code': 'G9', 'order': 3, 'age_range': '14-15 years'},
            
            # Senior Secondary
            {'level_code': 'SS', 'name': 'Grade 10', 'code': 'G10', 'order': 1, 'age_range': '15-16 years'},
            {'level_code': 'SS', 'name': 'Grade 11', 'code': 'G11', 'order': 2, 'age_range': '16-17 years'},
            {'level_code': 'SS', 'name': 'Grade 12', 'code': 'G12', 'order': 3, 'age_range': '17-18 years'},
            
            # University
            {'level_code': 'UNIV', 'name': 'Year 1', 'code': 'Y1', 'order': 1, 'age_range': '18-19 years'},
            {'level_code': 'UNIV', 'name': 'Year 2', 'code': 'Y2', 'order': 2, 'age_range': '19-20 years'},
            {'level_code': 'UNIV', 'name': 'Year 3', 'code': 'Y3', 'order': 3, 'age_range': '20-21 years'},
            {'level_code': 'UNIV', 'name': 'Year 4', 'code': 'Y4', 'order': 4, 'age_range': '21-22 years'},
        ]
        
        for grade_data in grades_data:
            level_code = grade_data.pop('level_code')
            education_level = EducationLevel.objects.get(code=level_code)
            
            grade, created = Grade.objects.get_or_create(
                education_level=education_level,
                code=grade_data['code'],
                defaults=grade_data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'  ✓ Created: {grade.name}'))
            else:
                self.stdout.write(f'  - Already exists: {grade.name}')

    def load_subjects(self):
        """Load CBC Subjects"""
        self.stdout.write('Loading Subjects...')
        
        subjects_data = [
            # Core subjects for all levels
            {
                'name': 'Mathematics',
                'code': 'MATH',
                'description': 'Mathematics and Numeracy',
                'is_core': True,
                'levels': ['PP', 'LP', 'UP', 'JS', 'SS']
            },
            {
                'name': 'English',
                'code': 'ENG',
                'description': 'English Language',
                'is_core': True,
                'levels': ['PP', 'LP', 'UP', 'JS', 'SS']
            },
            {
                'name': 'Kiswahili',
                'code': 'KSW',
                'description': 'Kiswahili Language',
                'is_core': True,
                'levels': ['PP', 'LP', 'UP', 'JS', 'SS']
            },
            
            # Pre-Primary and Primary
            {
                'name': 'Environmental Activities',
                'code': 'ENV',
                'description': 'Environmental Activities',
                'is_core': True,
                'levels': ['PP', 'LP']
            },
            {
                'name': 'Hygiene and Nutrition',
                'code': 'HYG',
                'description': 'Hygiene and Nutrition Activities',
                'is_core': True,
                'levels': ['PP', 'LP']
            },
            {
                'name': 'Religious Education',
                'code': 'CRE',
                'description': 'Christian Religious Education',
                'is_core': False,
                'levels': ['LP', 'UP', 'JS', 'SS']
            },
            {
                'name': 'Islamic Religious Education',
                'code': 'IRE',
                'description': 'Islamic Religious Education',
                'is_core': False,
                'levels': ['LP', 'UP', 'JS', 'SS']
            },
            {
                'name': 'Hindu Religious Education',
                'code': 'HRE',
                'description': 'Hindu Religious Education',
                'is_core': False,
                'levels': ['LP', 'UP', 'JS', 'SS']
            },
            
            # Upper Primary
            {
                'name': 'Integrated Science',
                'code': 'SCI',
                'description': 'Integrated Science',
                'is_core': True,
                'levels': ['UP']
            },
            {
                'name': 'Social Studies',
                'code': 'SST',
                'description': 'Social Studies',
                'is_core': True,
                'levels': ['UP']
            },
            {
                'name': 'Creative Arts',
                'code': 'CA',
                'description': 'Creative Arts and Sports',
                'is_core': False,
                'levels': ['PP', 'LP', 'UP']
            },
            
            # Junior Secondary
            {
                'name': 'Agriculture',
                'code': 'AGR',
                'description': 'Agriculture',
                'is_core': False,
                'levels': ['JS', 'SS']
            },
            {
                'name': 'Life Skills Education',
                'code': 'LSE',
                'description': 'Life Skills Education',
                'is_core': True,
                'levels': ['JS', 'SS']
            },
            
            # Sciences (Junior & Senior Secondary)
            {
                'name': 'Biology',
                'code': 'BIO',
                'description': 'Biology',
                'is_core': False,
                'levels': ['JS', 'SS']
            },
            {
                'name': 'Chemistry',
                'code': 'CHEM',
                'description': 'Chemistry',
                'is_core': False,
                'levels': ['JS', 'SS']
            },
            {
                'name': 'Physics',
                'code': 'PHY',
                'description': 'Physics',
                'is_core': False,
                'levels': ['JS', 'SS']
            },
            
            # Humanities (Junior & Senior Secondary)
            {
                'name': 'History',
                'code': 'HIST',
                'description': 'History',
                'is_core': False,
                'levels': ['JS', 'SS']
            },
            {
                'name': 'Geography',
                'code': 'GEO',
                'description': 'Geography',
                'is_core': False,
                'levels': ['JS', 'SS']
            },
            {
                'name': 'Business Studies',
                'code': 'BUS',
                'description': 'Business Studies',
                'is_core': False,
                'levels': ['JS', 'SS']
            },
            
            # Technical Subjects
            {
                'name': 'Computer Science',
                'code': 'COMP',
                'description': 'Computer Science',
                'is_core': False,
                'levels': ['JS', 'SS']
            },
            {
                'name': 'Home Science',
                'code': 'HSC',
                'description': 'Home Science',
                'is_core': False,
                'levels': ['JS', 'SS']
            },
            {
                'name': 'Design and Technology',
                'code': 'DT',
                'description': 'Design and Technology',
                'is_core': False,
                'levels': ['JS', 'SS']
            },
            {
                'name': 'Music',
                'code': 'MUS',
                'description': 'Music',
                'is_core': False,
                'levels': ['JS', 'SS']
            },
            {
                'name': 'Art and Design',
                'code': 'ART',
                'description': 'Art and Design',
                'is_core': False,
                'levels': ['JS', 'SS']
            },
            {
                'name': 'Physical Education',
                'code': 'PE',
                'description': 'Physical Education and Sports',
                'is_core': False,
                'levels': ['JS', 'SS']
            },
        ]
        
        for subject_data in subjects_data:
            level_codes = subject_data.pop('levels')
            
            subject, created = Subject.objects.get_or_create(
                code=subject_data['code'],
                defaults=subject_data
            )
            
            # Add education levels
            for level_code in level_codes:
                try:
                    level = EducationLevel.objects.get(code=level_code)
                    subject.education_levels.add(level)
                except EducationLevel.DoesNotExist:
                    pass
            
            if created:
                self.stdout.write(self.style.SUCCESS(f'  ✓ Created: {subject.name}'))
            else:
                self.stdout.write(f'  - Already exists: {subject.name}')