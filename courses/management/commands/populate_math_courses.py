from django.core.management.base import BaseCommand
from courses.models import Course


COURSES = [
    # ── Year 1 · Semester 1 ──────────────────────────────────────────────────
    ('ENGL101', 'Core English',              2, 1, 1),
    ('PHYS101', 'Core Physics',              4, 1, 1),
    ('INFT101', 'Information Technology',    2, 1, 1),
    ('PHE101',  'Physical Education',        2, 1, 1),
    ('AFST101', 'African Studies',           2, 1, 1),
    ('MATH111', 'Pre-Calculus',              4, 1, 1),
    ('MATH121', 'Introduction to Calculus',  4, 1, 1),
    ('MATH151', 'Applied Mathematics',       4, 1, 1),
    ('MATH171', 'Statistics',                4, 1, 1),
    ('MATH181', 'Introduction to Probability', 4, 1, 1),
    ('MATH191', 'Coordinate Geometry',       3, 1, 1),

    # ── Year 1 · Semester 2 ──────────────────────────────────────────────────
    ('ENGL102', 'Core English',              2, 1, 2),
    ('PHYS102', 'Core Physics',              4, 1, 2),
    ('INFT102', 'Information Technology',    2, 1, 2),
    ('PHE102',  'Physical Education',        2, 1, 2),
    ('AFST102', 'African Studies',           2, 1, 2),
    ('MATH112', 'Pre-Calculus',              4, 1, 2),
    ('MATH122', 'Calculus',                  4, 1, 2),
    ('MATH152', 'Applied Mathematics',       4, 1, 2),
    ('MATH172', 'Statistics',                4, 1, 2),
    ('MATH182', 'Probability',               4, 1, 2),
    ('MATH192', 'Coordinate Geometry 2',     3, 1, 2),

    # ── Year 2 · Semester 1 ──────────────────────────────────────────────────
    ('ENGL201', 'Core English',              2, 2, 1),
    ('INFT201', 'Information Technology',    2, 2, 1),
    ('MATH221', 'Integral Calculus',         4, 2, 1),
    ('MATH231', 'Abstract Algebra',          4, 2, 1),
    ('MATH241', 'Real Analysis',             4, 2, 1),
    ('MATH251', 'Applied Mathematics',       4, 2, 1),
    ('MATH271', 'Statistics',                3, 2, 1),
    ('MATH291', 'Geometry',                  2, 2, 1),

    # ── Year 2 · Semester 2 ──────────────────────────────────────────────────
    ('ENGL202', 'Core English',              2, 2, 2),
    ('INFT202', 'Information Technology',    2, 2, 2),
    ('MATH222', 'Calculus',                  4, 2, 2),
    ('MATH232', 'Abstract Algebra',          4, 2, 2),
    ('MATH242', 'Real Analysis',             4, 2, 2),
    ('MATH252', 'Applied Mathematics',       4, 2, 2),
    ('MATH272', 'Statistics',                3, 2, 2),
    ('MATH292', 'Geometry',                  2, 2, 2),

    # ── Year 3 · Semester 1 ──────────────────────────────────────────────────
    ('MATH321', 'Calculus',                  3, 3, 1),
    ('MATH341', 'Real Analysis',             3, 3, 1),
    ('MATH351', 'Applied Mathematics',       4, 3, 1),
    ('MATH361', 'Number Theory',             3, 3, 1),
    ('MATH381', 'Probability',               3, 3, 1),
    ('MATH391', 'Geometry',                  3, 3, 1),
    ('REMT301', 'Research Methods',          1, 3, 1),

    # ── Year 3 · Semester 2 ──────────────────────────────────────────────────
    ('MATH322', 'Calculus',                  4, 3, 2),
    ('MATH342', 'Real Analysis',             3, 3, 2),
    ('MATH352', 'Applied Mathematics',       3, 3, 2),
    ('MATH362', 'Number Theory',             3, 3, 2),
    ('MATH372', 'Statistics',                3, 3, 2),
    ('MATH392', 'Geometry',                  3, 3, 2),
    ('REMT302', 'Research Methods',          1, 3, 2),

    # ── Year 4 · Semester 1 (Internship — stored as a placeholder course) ────
    ('INTR401', 'Job Orientation / Internship', 20, 4, 1),

    # ── Year 4 · Semester 2 ──────────────────────────────────────────────────
    ('MATH422', 'Calculus',                  4, 4, 2),
    ('MATH432', 'Algebra',                   4, 4, 2),
    ('MATH462', 'Number Theory',             4, 4, 2),
    ('MATH472', 'Statistics',                4, 4, 2),
    ('MATH482', 'Probability',               4, 4, 2),
]

DESCRIPTIONS = {
    'MATH111': 'Elementary Set Theory, Relations and Functions, Linear and Quadratic Equations, Inequalities, Remainder and Factor Theorems, Mathematical Induction, Binomial Theorem.',
    'MATH121': 'Limits and Continuity, Differentiation by First Principles, Rules of Differentiation (Sum, Chain, Product, Quotient), Differentiation of Algebraic, Trigonometric, Exponential and Logarithmic Functions, Maxima & Minima.',
    'MATH151': 'Elementary Dynamics and Statics, Motion with Uniform Acceleration, Resolution and Resultants of Vectors, Graphical Representation of Data, Measures of Central Tendency.',
    'MATH171': 'Measures of Dispersion, Range, Interquartile Range, Variance, Standard Deviation, Coefficient of Variation, Standard Error of the Mean.',
    'MATH181': 'Factorials, Permutations and Combinations, Sample Space and Event Composition, Discrete Probability Distributions, Conditional Probability (Bayes Theorem), Continuous Probability Distributions.',
    'MATH191': 'Straight Lines, Distance Between Points, Midpoint of a Line Segment, Equations of a Straight Line, Circles, Tangents and Normals to a Circle.',
    'MATH112': 'Sequences and Series, Arithmetic Progression (AP), Geometric Progression (GP), Trigonometric Ratios, Matrices and Determinants, Introduction to Logic.',
    'MATH122': 'Applications to Differentiation (Curve Sketching), Integration (Definite and Indefinite Integrals), Integration Techniques, Approximate Methods of Integration.',
    'MATH152': 'Coplanar Forces in Equilibrium, General Conditions of Equilibrium, Lami\'s Theorem, Polygon of Forces.',
    'MATH172': 'Simple Sampling Theory, Sampling Distributions, Bivariate Data, Correlation and Regression, Product Moment Formula, Spearman\'s Rank Correlation.',
    'MATH182': 'Normal Distribution, Binomial, Poisson, Geometric and Hypergeometric Distributions.',
    'MATH192': 'The Parabola, Equation of the Parabola, Sketching, Tangents and Normals to a Parabola.',
    'MATH221': 'Derivatives of Trigonometric, Implicit, Exponential, Logarithmic and Inverse Functions; Leibnitz Theorem; Wallis Formula; Newton\'s Method; Integration of Trigonometric and Exponential Functions; Applications — Areas and Volumes.',
    'MATH231': 'Set Functions and Graphs, Arbitrary Cases of Membership, Cartesian Products, Equivalence and Partitions, Graphs of Harder Functions.',
    'MATH241': 'Set Theory — Naïve Point Set Theory, Equivalence Relations, Functions and Mapping.',
    'MATH251': 'Vectors and Scalars, Scalar and Vector Products, Displacement/Velocity/Acceleration as Vectors, Relative Velocity, Forces as Vectors, Parallelogram of Forces, Lami\'s Theorem.',
    'MATH271': 'Hypothesis Testing, Types of Error, Statistical Significance, Confidence Intervals, Power and Robustness, Degrees of Freedom, Non-parametric Analysis.',
    'MATH291': 'Conics — The Ellipse, The Hyperbola, Conic Sections, Tangents and Normals to Conic Sections.',
    'MATH222': 'Partial Differentiation, Chain Rules, Total Differential, Maxima and Minima of Functions of Two Variables, Differential Equations (1st and 2nd Order), Applications in Science and Engineering.',
    'MATH232': 'Matrix Operations, Rank of a Matrix, Matrix Inverses, Systems of Linear Equations.',
    'MATH242': 'Inequalities, Cauchy Triangle Inequality, Sequences (Convergence, Monotonic), Series (Supremum, Limit Infimum, Cauchy Sequences), Comparison/Ratio/Root Tests.',
    'MATH252': 'Forces — Polygon of Forces, Moments and Couples, Reduction of Coplanar Forces, Projectiles, Newton\'s Laws of Motion.',
    'MATH272': 'The Normal Distribution, Areas Under the Standard Normal Curve, Normal Approximations to the Binomial Distribution.',
    'MATH292': 'Incidence Geometry in Planes and Space, Distance and Congruence, Congruencies Between Triangles, Hyperbolic Geometry, Euclidean Geometry.',
    'MATH321': 'Differentiation of Sums and Products, Function of a Power Series, Rolle\'s Theorem, First Mean Value Theorem, Leibnitz Theorem, Taylor\'s Theorem, L\'Hôpital\'s Theorem.',
    'MATH341': 'Cantor\'s Diagonal Process, Natural Numbers, Negative and Fractional Numbers, Countability of Rationals, Dedekind\'s Cuts, Supremum and Infimum.',
    'MATH351': 'Gravity and Friction, Centre of Gravity, Work Energy and Power, Principle of Conservation of Energy and Momentum, Impulsive Motion, Oblique Impact.',
    'MATH361': 'Integers — Axioms, Division Algorithm, GCD and LCM, Euclidean Algorithm, Euclid\'s Lemma.',
    'MATH381': 'Various Probability Distributions — Binomial, Poisson, Multinomial, Uniform, Exponential, Normal.',
    'MATH391': 'Analytical Geometry — Coordinates and Loci, Transformation of Coordinates, Polar Coordinates.',
    'REMT301': 'Introduction to Research Methodology for Mathematics.',
    'MATH322': 'Riemann\'s Integral, Multiple Integration, Double and Triple Integrals, Change of Variables, Centre of Mass, Moments of Inertia, Surface Area.',
    'MATH342': 'Continuity of Functions, Power Series with Radius of Convergence, Uniform Convergence, Heine-Borel Theorem.',
    'MATH352': 'Vectors — Differentiation of a Unit Vector, Motion in a Circle, Simple Harmonic Motion, Dynamics of a Rigid Body Fixed Axis, Normal Modes.',
    'MATH362': 'Algorithms, Integers and Division, Integers and Algorithms, Applications.',
    'MATH372': 'Variance Tests, Chi-Square Test, F-Tests, Wilcoxon Rank Sum / Mann-Whitney U Test, Contingency Tables, Fisher\'s Exact Test, McNemar\'s Test.',
    'MATH392': 'Axiomatic Geometry — Axioms, Theorems and Proofs.',
    'REMT302': 'Advanced Research Methods and Project Proposal Writing.',
    'INTR401': 'Job Orientation and Industrial Experience / Internship.',
    'MATH422': 'Triple Integrals in Cylindrical and Spherical Coordinates, Jacobians, Beta Function, Gamma Function, Vector Analysis, Green\'s Theorem, Parametric Surfaces.',
    'MATH432': 'Groups and Matrices, Geometric Transformations, Permutations, Subgroups, Cyclic Groups, Lagrange\'s Theorem, Homomorphism, Normal Subgroup, Isomorphism Theorems.',
    'MATH462': 'Congruence and Residue Classes, Composition of Functions and Permutations.',
    'MATH472': 'Analysis of Variance, One-Way ANOVA, Two-Way and Higher-Way ANOVA, Block and Fractional Designs, Methods of Sampling.',
    'MATH482': 'Limit Theorems, Law of Large Numbers, Chebyshev\'s Inequality.',
}


class Command(BaseCommand):
    help = 'Populate the database with all B.Sc. Mathematics courses from the ETU curriculum'

    def add_arguments(self, parser):
        parser.add_argument(
            '--year', type=str, default='2024/2025',
            help='Academic year to assign (default: 2024/2025)',
        )
        parser.add_argument(
            '--clear', action='store_true',
            help='Delete existing courses before inserting',
        )

    def handle(self, *args, **options):
        academic_year = options['year']

        if options['clear']:
            deleted, _ = Course.objects.all().delete()
            self.stdout.write(self.style.WARNING(f'Cleared {deleted} existing courses.'))

        created = 0
        updated = 0

        for code, name, credits, year, sem in COURSES:
            desc = DESCRIPTIONS.get(code, '')
            course, is_new = Course.objects.update_or_create(
                code=code,
                defaults={
                    'name': name,
                    'credits': credits,
                    'year_of_study': year,
                    'semester': str(sem),
                    'academic_year': academic_year,
                    'description': desc,
                    'is_active': True,
                    'max_students': 60,
                },
            )
            if is_new:
                created += 1
            else:
                updated += 1

        self.stdout.write(
            self.style.SUCCESS(
                f'Done. Created: {created}  Updated: {updated}  '
                f'Total: {Course.objects.count()} courses in database.'
            )
        )
