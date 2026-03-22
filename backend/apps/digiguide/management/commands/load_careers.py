"""
Django management command to load KUCCPS career data
"""
from django.core.management.base import BaseCommand
from apps.digiguide.models import Cluster, ClusterSubjectRequirement, Career, Subject


class Command(BaseCommand):
    help = 'Load KUCCPS career data (Clusters, Requirements, and Careers)'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.NOTICE('Loading KUCCPS career data...'))
        
        # Load Clusters
        self.load_clusters()
        
        # Load Cluster Subject Requirements
        self.load_cluster_requirements()
        
        # Load Sample Careers
        self.load_careers()
        
        self.stdout.write(self.style.SUCCESS('Successfully loaded KUCCPS career data!'))

    def load_clusters(self):
        """Load KUCCPS Clusters"""
        self.stdout.write('Loading KUCCPS Clusters...')
        
        clusters = [
            {
                'name': 'Cluster 1: Engineering and Technology',
                'code': 'CLUSTER_1',
                'description': 'Engineering, Architecture, Building & Construction, Surveying'
            },
            {
                'name': 'Cluster 2: Biological and Physical Sciences',
                'code': 'CLUSTER_2',
                'description': 'Pure Sciences, Applied Sciences, Statistics, Actuarial Science'
            },
            {
                'name': 'Cluster 3: Agriculture, Veterinary and Related',
                'code': 'CLUSTER_3',
                'description': 'Agriculture, Horticulture, Veterinary Medicine, Animal Health'
            },
            {
                'name': 'Cluster 4: Medicine and Health Sciences',
                'code': 'CLUSTER_4',
                'description': 'Medicine, Nursing, Pharmacy, Dentistry, Clinical Medicine'
            },
            {
                'name': 'Cluster 5: Economics, Commerce and Related',
                'code': 'CLUSTER_5',
                'description': 'Economics, Commerce, Business Administration, Accounting'
            },
            {
                'name': 'Cluster 6: Education',
                'code': 'CLUSTER_6',
                'description': 'Education (Arts), Education (Science), Early Childhood Education'
            },
            {
                'name': 'Cluster 7: Arts and Humanities',
                'code': 'CLUSTER_7',
                'description': 'Literature, Languages, History, Philosophy, Religion'
            },
            {
                'name': 'Cluster 8: Social Sciences',
                'code': 'CLUSTER_8',
                'description': 'Law, Journalism, Psychology, Sociology, Political Science'
            },
            {
                'name': 'Cluster 9: Hospitality and Tourism',
                'code': 'CLUSTER_9',
                'description': 'Hotel Management, Tourism Management, Catering, Travel'
            },
        ]
        
        for cluster_data in clusters:
            cluster, created = Cluster.objects.get_or_create(
                code=cluster_data['code'],
                defaults=cluster_data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'  ✓ Created: {cluster.name}'))
            else:
                self.stdout.write(f'  - Already exists: {cluster.name}')

    def load_cluster_requirements(self):
        """Load Cluster Subject Requirements"""
        self.stdout.write('Loading Cluster Subject Requirements...')
        
        requirements = [
            # Cluster 1: Engineering
            {'cluster': 'CLUSTER_1', 'subject': 'MATH', 'min_grade': 'B', 'is_mandatory': True},
            {'cluster': 'CLUSTER_1', 'subject': 'PHY', 'min_grade': 'B', 'is_mandatory': True},
            {'cluster': 'CLUSTER_1', 'subject': 'CHEM', 'min_grade': 'C+', 'is_mandatory': False},
            {'cluster': 'CLUSTER_1', 'subject': 'ENG', 'min_grade': 'C+', 'is_mandatory': True},
            
            # Cluster 2: Sciences
            {'cluster': 'CLUSTER_2', 'subject': 'MATH', 'min_grade': 'B', 'is_mandatory': True},
            {'cluster': 'CLUSTER_2', 'subject': 'PHY', 'min_grade': 'B', 'is_mandatory': True},
            {'cluster': 'CLUSTER_2', 'subject': 'CHEM', 'min_grade': 'B', 'is_mandatory': True},
            {'cluster': 'CLUSTER_2', 'subject': 'BIO', 'min_grade': 'C+', 'is_mandatory': False},
            
            # Cluster 3: Agriculture
            {'cluster': 'CLUSTER_3', 'subject': 'BIO', 'min_grade': 'B', 'is_mandatory': True},
            {'cluster': 'CLUSTER_3', 'subject': 'CHEM', 'min_grade': 'B', 'is_mandatory': True},
            {'cluster': 'CLUSTER_3', 'subject': 'MATH', 'min_grade': 'C+', 'is_mandatory': False},
            {'cluster': 'CLUSTER_3', 'subject': 'AGR', 'min_grade': 'C+', 'is_mandatory': False},
            
            # Cluster 4: Medicine
            {'cluster': 'CLUSTER_4', 'subject': 'BIO', 'min_grade': 'B+', 'is_mandatory': True},
            {'cluster': 'CLUSTER_4', 'subject': 'CHEM', 'min_grade': 'B+', 'is_mandatory': True},
            {'cluster': 'CLUSTER_4', 'subject': 'PHY', 'min_grade': 'B', 'is_mandatory': True},
            {'cluster': 'CLUSTER_4', 'subject': 'MATH', 'min_grade': 'B', 'is_mandatory': True},
            {'cluster': 'CLUSTER_4', 'subject': 'ENG', 'min_grade': 'B', 'is_mandatory': True},
            
            # Cluster 5: Economics/Commerce
            {'cluster': 'CLUSTER_5', 'subject': 'MATH', 'min_grade': 'B', 'is_mandatory': True},
            {'cluster': 'CLUSTER_5', 'subject': 'ENG', 'min_grade': 'B', 'is_mandatory': True},
            {'cluster': 'CLUSTER_5', 'subject': 'BUS', 'min_grade': 'C+', 'is_mandatory': False},
            
            # Cluster 6: Education
            {'cluster': 'CLUSTER_6', 'subject': 'ENG', 'min_grade': 'C+', 'is_mandatory': True},
            {'cluster': 'CLUSTER_6', 'subject': 'MATH', 'min_grade': 'C+', 'is_mandatory': False},
            
            # Cluster 7: Arts
            {'cluster': 'CLUSTER_7', 'subject': 'ENG', 'min_grade': 'B', 'is_mandatory': True},
            {'cluster': 'CLUSTER_7', 'subject': 'KSW', 'min_grade': 'C+', 'is_mandatory': False},
            {'cluster': 'CLUSTER_7', 'subject': 'HIST', 'min_grade': 'C+', 'is_mandatory': False},
            
            # Cluster 8: Social Sciences
            {'cluster': 'CLUSTER_8', 'subject': 'ENG', 'min_grade': 'B', 'is_mandatory': True},
            {'cluster': 'CLUSTER_8', 'subject': 'HIST', 'min_grade': 'C+', 'is_mandatory': False},
            {'cluster': 'CLUSTER_8', 'subject': 'GEO', 'min_grade': 'C+', 'is_mandatory': False},
            
            # Cluster 9: Hospitality
            {'cluster': 'CLUSTER_9', 'subject': 'ENG', 'min_grade': 'C+', 'is_mandatory': True},
            {'cluster': 'CLUSTER_9', 'subject': 'MATH', 'min_grade': 'C', 'is_mandatory': False},
        ]
        
        for req_data in requirements:
            try:
                cluster = Cluster.objects.get(code=req_data['cluster'])
                subject = Subject.objects.get(code=req_data['subject'])
                
                requirement, created = ClusterSubjectRequirement.objects.get_or_create(
                    cluster=cluster,
                    subject=subject,
                    defaults={
                        'minimum_grade': req_data['min_grade'],
                        'is_mandatory': req_data['is_mandatory']
                    }
                )
                if created:
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'  ✓ Added requirement: {subject.name} ({req_data["min_grade"]}) for {cluster.name}'
                        )
                    )
            except (Cluster.DoesNotExist, Subject.DoesNotExist) as e:
                self.stdout.write(self.style.WARNING(f'  ⚠ Skipped: {str(e)}'))

    def load_careers(self):
        """Load Sample Careers"""
        self.stdout.write('Loading Sample Careers...')
        
        careers = [
            # Cluster 1: Engineering
            {
                'name': 'Bachelor of Engineering (Mechanical)',
                'cluster': 'CLUSTER_1',
                'description': 'Design, develop and maintain mechanical systems and machinery',
                'required_qualifications': 'KCSE Mean Grade B+ with B in Math, Physics; C+ in Chemistry/Physical Sciences',
                'job_outlook': 'Mechanical Engineer, Design Engineer, Manufacturing Engineer, Maintenance Engineer',
                'related_courses': 'Mechanical Engineering, Manufacturing Engineering, Mechatronics',
                'industry': 'Engineering & Manufacturing'
            },
            {
                'name': 'Bachelor of Engineering (Civil)',
                'cluster': 'CLUSTER_1',
                'description': 'Plan, design and oversee construction of buildings and infrastructure',
                'required_qualifications': 'KCSE Mean Grade B+ with B in Math, Physics; C+ in Chemistry/Physical Sciences',
                'job_outlook': 'Civil Engineer, Structural Engineer, Construction Manager, Project Engineer',
                'related_courses': 'Civil Engineering, Structural Engineering, Construction Management',
                'industry': 'Engineering & Construction'
            },
            {
                'name': 'Bachelor of Engineering (Electrical)',
                'cluster': 'CLUSTER_1',
                'description': 'Design and develop electrical systems and equipment',
                'required_qualifications': 'KCSE Mean Grade B+ with B in Math, Physics; C+ in Chemistry/Physical Sciences',
                'job_outlook': 'Electrical Engineer, Power Systems Engineer, Electronics Engineer, Control Systems Engineer',
                'related_courses': 'Electrical Engineering, Electronics Engineering, Power Systems',
                'industry': 'Engineering & Technology'
            },
            
            # Cluster 2: Sciences
            {
                'name': 'Bachelor of Science (Computer Science)',
                'cluster': 'CLUSTER_2',
                'description': 'Study of computation, information processing, and software systems',
                'required_qualifications': 'KCSE Mean Grade B with B in Math; C+ in Physics',
                'job_outlook': 'Software Developer, Data Scientist, Systems Analyst, IT Consultant',
                'related_courses': 'Computer Science, Information Technology, Software Engineering',
                'industry': 'Technology & IT'
            },
            {
                'name': 'Bachelor of Science (Mathematics)',
                'cluster': 'CLUSTER_2',
                'description': 'Advanced mathematical theory and applications',
                'required_qualifications': 'KCSE Mean Grade B with B in Math; C+ in Physics',
                'job_outlook': 'Mathematician, Statistician, Actuary, Data Analyst, Researcher',
                'related_courses': 'Mathematics, Statistics, Actuarial Science',
                'industry': 'Finance & Research'
            },
            
            # Cluster 3: Agriculture
            {
                'name': 'Bachelor of Science (Agriculture)',
                'cluster': 'CLUSTER_3',
                'description': 'Modern agricultural practices and crop production',
                'required_qualifications': 'KCSE Mean Grade C+ with C+ in Biology, Chemistry; C in Math/Physics',
                'job_outlook': 'Agricultural Officer, Farm Manager, Agronomist, Agricultural Consultant',
                'related_courses': 'Agriculture, Agribusiness, Horticulture',
                'industry': 'Agriculture'
            },
            {
                'name': 'Bachelor of Veterinary Medicine',
                'cluster': 'CLUSTER_3',
                'description': 'Diagnosis and treatment of animal diseases',
                'required_qualifications': 'KCSE Mean Grade B with B in Biology, Chemistry; C+ in Math/Physics',
                'job_outlook': 'Veterinarian, Animal Health Officer, Veterinary Surgeon, Research Scientist',
                'related_courses': 'Veterinary Medicine, Animal Health, Animal Science',
                'industry': 'Veterinary & Animal Health'
            },
            
            # Cluster 4: Medicine
            {
                'name': 'Bachelor of Medicine and Surgery (MBChB)',
                'cluster': 'CLUSTER_4',
                'description': 'Medical education for diagnosing and treating human diseases',
                'required_qualifications': 'KCSE Mean Grade A- with B+ in Biology, Chemistry, Physics; B in Math, English',
                'job_outlook': 'Medical Doctor, Surgeon, Physician, Medical Researcher, Consultant',
                'related_courses': 'Medicine and Surgery, Clinical Medicine, Medical Sciences',
                'industry': 'Healthcare & Medicine',
                'salary_range': 'KES 150,000 - 500,000'
            },
            {
                'name': 'Bachelor of Pharmacy',
                'cluster': 'CLUSTER_4',
                'description': 'Pharmaceutical sciences and drug dispensation',
                'required_qualifications': 'KCSE Mean Grade B with B in Biology, Chemistry; C+ in Math/Physics',
                'job_outlook': 'Pharmacist, Pharmaceutical Analyst, Drug Inspector, Hospital Pharmacist',
                'related_courses': 'Pharmacy, Pharmaceutical Sciences',
                'industry': 'Healthcare & Pharmaceuticals',
                'salary_range': 'KES 80,000 - 250,000'
            },
            {
                'name': 'Bachelor of Nursing',
                'cluster': 'CLUSTER_4',
                'description': 'Patient care and nursing practice',
                'required_qualifications': 'KCSE Mean Grade C+ with C+ in Biology, Chemistry; C in English, Math',
                'job_outlook': 'Registered Nurse, Nurse Practitioner, Clinical Nurse, Public Health Nurse',
                'related_courses': 'Nursing, Clinical Nursing, Public Health Nursing',
                'industry': 'Healthcare',
                'salary_range': 'KES 50,000 - 150,000'
            },
            
            # Cluster 5: Economics/Commerce
            {
                'name': 'Bachelor of Commerce',
                'cluster': 'CLUSTER_5',
                'description': 'Business, accounting, finance and commercial activities',
                'required_qualifications': 'KCSE Mean Grade C+ with C+ in Math, English; C in any Group II/III',
                'job_outlook': 'Accountant, Business Analyst, Financial Analyst, Marketing Manager',
                'related_courses': 'Commerce, Accounting, Finance, Business Administration',
                'industry': 'Business & Finance',
                'salary_range': 'KES 60,000 - 200,000'
            },
            {
                'name': 'Bachelor of Economics',
                'cluster': 'CLUSTER_5',
                'description': 'Economic theory and analysis',
                'required_qualifications': 'KCSE Mean Grade B with B in Math; C+ in English',
                'job_outlook': 'Economist, Policy Analyst, Research Economist, Financial Consultant',
                'related_courses': 'Economics, Applied Economics, Economic Policy',
                'industry': 'Economics & Policy',
                'salary_range': 'KES 70,000 - 250,000'
            },
            
            # Cluster 6: Education
            {
                'name': 'Bachelor of Education (Science)',
                'cluster': 'CLUSTER_6',
                'description': 'Training to teach science subjects in secondary schools',
                'required_qualifications': 'KCSE Mean Grade C+ with C+ in two teaching subjects; C in English',
                'job_outlook': 'Secondary School Teacher, Education Officer, Curriculum Developer, Tutor',
                'related_courses': 'Education (Science), Science Education, Teaching Methods',
                'industry': 'Education',
                'salary_range': 'KES 40,000 - 100,000'
            },
            {
                'name': 'Bachelor of Education (Arts)',
                'cluster': 'CLUSTER_6',
                'description': 'Training to teach arts subjects in secondary schools',
                'required_qualifications': 'KCSE Mean Grade C+ with C+ in two teaching subjects; C in English',
                'job_outlook': 'Secondary School Teacher, Education Officer, Curriculum Developer, Tutor',
                'related_courses': 'Education (Arts), Arts Education, Teaching Methods',
                'industry': 'Education',
                'salary_range': 'KES 40,000 - 100,000'
            },
            
            # Cluster 7: Arts
            {
                'name': 'Bachelor of Arts (English & Literature)',
                'cluster': 'CLUSTER_7',
                'description': 'Study of English language and literature',
                'required_qualifications': 'KCSE Mean Grade C+ with C+ in English, Kiswahili; C in any Group II/III/IV',
                'job_outlook': 'Writer, Editor, Journalist, Content Creator, Language Teacher',
                'related_courses': 'English Literature, Creative Writing, Communication',
                'industry': 'Arts & Media',
                'salary_range': 'KES 40,000 - 150,000'
            },
            {
                'name': 'Bachelor of Arts (History)',
                'cluster': 'CLUSTER_7',
                'description': 'Study of historical events and civilizations',
                'required_qualifications': 'KCSE Mean Grade C+ with C+ in History, English; C in any Group II/III',
                'job_outlook': 'Historian, Museum Curator, Archivist, Researcher, Teacher',
                'related_courses': 'History, Archaeology, Heritage Studies',
                'industry': 'Arts & Heritage',
                'salary_range': 'KES 45,000 - 120,000'
            },
            
            # Cluster 8: Social Sciences
            {
                'name': 'Bachelor of Laws (LLB)',
                'cluster': 'CLUSTER_8',
                'description': 'Study of legal systems and jurisprudence',
                'required_qualifications': 'KCSE Mean Grade B with B in English; C+ in any two Group II/III/IV',
                'job_outlook': 'Lawyer, Advocate, Legal Officer, Magistrate, Legal Consultant',
                'related_courses': 'Law, Legal Studies, International Law',
                'industry': 'Legal & Justice',
                'salary_range': 'KES 100,000 - 500,000'
            },
            {
                'name': 'Bachelor of Journalism and Mass Communication',
                'cluster': 'CLUSTER_8',
                'description': 'Media studies and communication',
                'required_qualifications': 'KCSE Mean Grade C+ with C+ in English, Kiswahili; C in any Group III/IV',
                'job_outlook': 'Journalist, News Reporter, Media Producer, Public Relations Officer',
                'related_courses': 'Journalism, Mass Communication, Media Studies',
                'industry': 'Media & Communication',
                'salary_range': 'KES 50,000 - 200,000'
            },
            
            # Cluster 9: Hospitality
            {
                'name': 'Bachelor of Hospitality Management',
                'cluster': 'CLUSTER_9',
                'description': 'Hotel and hospitality industry management',
                'required_qualifications': 'KCSE Mean Grade C+ with C+ in English, Math; C in any Group III/IV',
                'job_outlook': 'Hotel Manager, Restaurant Manager, Event Planner, Tourism Officer',
                'related_courses': 'Hospitality Management, Hotel Management, Tourism',
                'industry': 'Hospitality & Tourism',
                'salary_range': 'KES 50,000 - 180,000'
            },
            {
                'name': 'Bachelor of Tourism Management',
                'cluster': 'CLUSTER_9',
                'description': 'Tourism industry and travel services management',
                'required_qualifications': 'KCSE Mean Grade C+ with C+ in English; C in Math, Geography',
                'job_outlook': 'Tourism Manager, Tour Guide, Travel Consultant, Destination Manager',
                'related_courses': 'Tourism Management, Travel & Tourism, Ecotourism',
                'industry': 'Tourism & Travel',
                'salary_range': 'KES 45,000 - 150,000'
            },
        ]
        
        for career_data in careers:
            cluster_code = career_data.pop('cluster')
            try:
                cluster = Cluster.objects.get(code=cluster_code)
                career, created = Career.objects.get_or_create(
                    name=career_data['name'],
                    defaults={**career_data, 'cluster': cluster}
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f'  ✓ Created: {career.name}'))
                else:
                    self.stdout.write(f'  - Already exists: {career.name}')
            except Cluster.DoesNotExist:
                self.stdout.write(self.style.WARNING(f'  ⚠ Cluster {cluster_code} not found'))