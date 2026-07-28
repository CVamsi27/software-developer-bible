[![Category: Interview](https://img.shields.io/badge/category-Interview-1f7a8a)](.)

# DevOps, Behavioral & Career Preparation (Phases 20–28)

---

# Phase 20: Git & Version Control

> **Why It Matters:** Git is the industry standard for version control. Interviewers expect you to know branching strategies, conflict resolution, and advanced commands.

## Essential Git Commands

```bash
# Basic Workflow
git init                    # Initialize repository
git clone <url>             # Clone remote repository
git add .                   # Stage all changes
git add <file>              # Stage specific file
git commit -m "message"     # Commit with message
git push origin main        # Push to remote
git pull origin main        # Pull from remote

# Branching
git branch                  # List local branches
git branch -a               # List all branches (including remote)
git branch <name>           # Create new branch
git checkout <name>         # Switch to branch
git checkout -b <name>      # Create and switch to branch
git switch <name>           # Switch to branch (modern)
git switch -c <name>        # Create and switch (modern)
git branch -d <name>        # Delete branch (safe)
git branch -D <name>        # Delete branch (force)

# Merging
git merge <branch>          # Merge branch into current
git merge --abort           # Abort merge
git merge --squash <branch> # Squash merge (combine commits)

# Rebase
git rebase <branch>         # Rebase current branch onto branch
git rebase -i HEAD~5        # Interactive rebase last 5 commits
git rebase --abort          # Abort rebase
git rebase --continue       # Continue after resolving conflicts

# Stashing
git stash                   # Stash current changes
git stash list              # List stashes
git stash pop               # Apply and remove stash
git stash apply             # Apply stash without removing
git stash drop              # Remove stash

# History & Inspection
git log                     # View commit history
git log --oneline --graph   # Compact graph view
git log --author="name"     # Filter by author
git log --since="2024-01-01" # Filter by date
git diff                    # Unstaged changes
git diff --staged           # Staged changes
git diff branch1..branch2   # Compare branches
git show <commit>           # Show commit details
git blame <file>            # Line-by-line history

# Undoing Changes
git reset HEAD <file>       # Unstage file
git reset --soft HEAD~1     # Undo commit, keep changes staged
git reset --mixed HEAD~1    # Undo commit, keep changes unstaged
git reset --hard HEAD~1     # Undo commit, discard changes
git revert <commit>         # Create new commit that undoes changes
git restore <file>          # Discard changes (modern)

# Cherry Pick
git cherry-pick <commit>    # Apply specific commit to current branch

# Advanced
git reflog                  # View all reference updates
git bisect start            # Binary search for bug
git bisect bad              # Mark current commit as bad
git bisect good <commit>    # Mark commit as good

```

## Merge vs Rebase

```text

Merge:
- Creates merge commit
- Preserves history
- Safe for shared branches
- Use when: collaborating on feature branches

Rebase:
- Linear history
- Cleaner git log
- Rewrites history (dangerous on shared branches)
- Use when: cleaning up before merging to main

When to Use What:
- Feature branch → develop: Merge (preserves context)
- Cleaning up commits: Rebase (linear history)
- Updating feature branch with main: Rebase (avoid merge commits)
- Shared/public branch: Never rebase

```

## Git Hooks

```bash
# .git/hooks/pre-commit — runs before commit
#!/bin/sh
npm run lint
npm run test

# .git/hooks/commit-msg — validates commit message
#!/bin/sh
commit_msg=$(cat "$1")
if ! echo "$commit_msg" | grep -qE "^(feat|fix|docs|style|refactor|test|chore):"; then
    echo "Commit message must follow conventional commits format"
    exit 1
fi

# Husky (Node.js) — modern git hooks
npx husky init
echo "npm run lint" > .husky/pre-commit

```

## Branching Strategies

```text

Git Flow:
- main (production)
- develop (integration)
- feature/* (new features)
- release/* (release preparation)
- hotfix/* (production fixes)

GitHub Flow:
- main (production-ready)
- feature branches → PR → merge to main

Trunk-Based Development:
- main (always deployable)
- Short-lived feature branches (< 1 day)
- Feature flags for incomplete features

```

### Resources for Git

- 📘 **Book:** *Pro Git* by Scott Chacon (free online)
- 🌐 **Website:** [Git Documentation](https://git-scm.com/doc)
- 🌐 **Website:** [Git Immersion](https://gitimmersion.com/) — guided tour
- 🌐 **Website:** [Learn Git Branching](https://learngitbranching.js.org/) — interactive
- 🎥 **YouTube:** [Fireship](https://www.youtube.com/@Fireship) — Git in 100 seconds

---

# Phase 21: Linux & Shell

> **Why It Matters:** Most servers run Linux. Basic shell proficiency is expected for debugging, monitoring, and deployment tasks.

## Essential Commands

```bash
# File Operations
ls -la                    # List all files with details
ls -lh                    # Human-readable sizes
find /path -name "*.java" # Find files by name
find /path -mtime -7      # Modified in last 7 days
find /path -size +100M    # Files larger than 100MB
cp -r source/ dest/       # Copy directory recursively
mv old new                # Move/rename
rm -rf directory/          # Remove directory recursively
mkdir -p path/to/dir      # Create nested directories
touch file                # Create empty file
ln -s target link         # Create symbolic link

# Text Processing
cat file                  # Print file contents
head -n 20 file           # First 20 lines
tail -n 20 file           # Last 20 lines
tail -f file              # Follow file (live updates)
grep "pattern" file       # Search for pattern
grep -r "pattern" dir/    # Recursive search
grep -i "pattern" file    # Case-insensitive
grep -n "pattern" file    # Show line numbers
grep -c "pattern" file    # Count matches
sed 's/old/new/g' file    # Replace text
awk '{print $1}' file     # Print first column
cut -d',' -f1,3 file      # Extract columns 1 and 3
sort file                 # Sort lines
uniq -c                   # Count unique lines
wc -l file                # Count lines

# Process Management
ps aux                    # All running processes
ps aux | grep java        # Find Java processes
top                       # Real-time process monitor
htop                      # Interactive process monitor
kill <pid>                # Send SIGTERM
kill -9 <pid>             # Send SIGKILL
nohup command &           # Run in background
jobs                      # List background jobs
fg %1                     # Bring job to foreground

# Disk & Memory
df -h                     # Disk space usage
du -sh /path              # Directory size
free -h                   # Memory usage
lsof -i :8080             # What's using port 8080

# Networking
curl -I url               # HTTP headers
curl -X POST url -d '{}'  # POST request
ping host                 # Test connectivity
traceroute host           # Trace network path
netstat -tlnp             # Listening ports
ss -tlnp                  # Socket statistics (modern)
wget url                  # Download file
scp file user@host:path   # Secure copy
ssh user@host             # Secure shell

# Permissions
chmod 755 file            # rwxr-xr-x
chmod u+x script          # Add execute for user
chown user:group file     # Change ownership

# System
uname -a                  # System information
whoami                    # Current user
uptime                    # System uptime
dmesg                     # Kernel messages
journalctl -u service     # Service logs
systemctl status service  # Service status
systemctl start service   # Start service
systemctl stop service    # Stop service

```

## Shell Scripting

```bash
#!/bin/bash

# Variables
NAME="World"
echo "Hello, $NAME"

# Conditional
if [ -f "file.txt" ]; then
    echo "File exists"
elif [ -d "directory" ]; then
    echo "Directory exists"
else
    echo "Neither exists"
fi

# Loops
for i in {1..10}; do
    echo $i
done

for file in *.java; do
    echo "Processing $file"
done

# Functions
process_file() {
    local filename=$1
    echo "Processing $filename"
    return 0
}

process_file "myfile.txt"

# Array
arr=("one" "two" "three")
echo ${arr[0]}        # first element
echo ${arr[@]}        # all elements
echo ${#arr[@]}       # length

# Case statement
case $1 in
    start)
        echo "Starting..."
        ;;
    stop)
        echo "Stopping..."
        ;;
    *)
        echo "Usage: $0 {start|stop}"
        ;;
esac

# Error handling
set -e  # Exit on error
set -u  # Treat unset variables as errors
trap 'echo "Error on line $LINENO"' ERR

```

##管道和重定向

```bash
# Pipes
cat file.txt | grep "error" | sort | uniq -c | sort -rn

# Redirection
command > file        # stdout to file (overwrite)
command >> file       # stdout to file (append)
command 2> error.txt  # stderr to file
command &> all.txt    # both stdout and stderr
command < input.txt   # stdin from file

# Here document
cat << EOF
Line 1
Line 2
EOF

# Process substitution
diff <(sort file1) <(sort file2)

```

### Resources for Linux

- 📘 **Book:** *The Linux Command Line* by William Shotts (free online)
- 📘 **Book:** *Unix and Linux System Administration Handbook*
- 🌐 **Website:** [Linux Journey](https://linuxjourney.com/) — free interactive course
- 🌐 **Website:** [OverTheWire: Bandit](https://overthewire.org/wargames/bandit/) — learn by doing
- 🌐 **Website:** [explainshell.com](https://explainshell.com/) — explain commands
- 🎥 **YouTube:** [NetworkChuck](https://www.youtube.com/@NetworkChuck) — Linux tutorials

---

# Phase 22: Behavioral Interviews

> **Why It Matters:** Behavioral interviews assess your soft skills, leadership, conflict resolution, and cultural fit. At top companies, behavioral performance can be the deciding factor.

## The STAR Method

```text

S — Situation: Set the context (brief, relevant)
T — Task: Describe your specific responsibility
A — Action: Detail what YOU did (use "I", not "we")
R — Result: Quantify the outcome and what you learned

```

### Example: Conflict Resolution

```text

S: "In my previous role, I was working on a critical payment feature with
    a senior engineer who insisted on using a complex event-driven architecture.
    I believed a simpler synchronous approach would be faster to implement."

T: "I needed to convince my teammate while maintaining our working relationship
    and meeting our deadline."

A: "I scheduled a 1:1 meeting and asked him to walk me through his approach.
    I listened carefully and identified valid concerns about scalability.
    I then proposed a hybrid approach: synchronous now, with an event-driven
    migration path for later. I created a simple proof-of-concept that
    demonstrated the performance difference."

R: "We went with the hybrid approach. The feature shipped 2 weeks ahead of
    schedule, and the simplified architecture reduced bugs by 40%. My teammate
    and I now have a great working relationship and often collaborate on
    design decisions."

```

## Amazon Leadership Principles

```text

1.  Customer Obsession — Start with customer, work backwards
2.  Ownership — Think long-term, act on behalf of the company
3.  Invent and Simplify — Innovate and find ways to simplify
4.  Are Right, A Lot — Good judgment, seek diverse perspectives
5.  Learn and Be Curious — Always learning, exploring
6.  Hire and Develop the Best — Raise the performance bar
7.  Insist on the Highest Standards — Never settle
8.  Think Big — Create bold direction that inspires
9.  Bias for Action — Speed matters in business
10. Frugality — Accomplish more with less
11. Earn Trust — Listen, speak candidly, treat others respectfully
12. Dive Deep — Stay connected to details
13. Have Backbone; Disagree and Commit — Respectfully challenge, commit fully
14. Deliver Results — Focus on key inputs, deliver with quality

```

## Microsoft Growth Mindset

```text

Key Themes:
- Learning from failure and iterating
- Embracing challenges and ambiguity
- Collaborative problem-solving
- Empathy and inclusion
- Continuous improvement

Example Stories to Prepare:
1. A time you failed and what you learned
2. How you handled ambiguity in a project
3. How you helped a struggling teammate
4. A time you challenged the status quo
5. How you adapted to changing requirements

```

## Common Behavioral Questions

### Leadership & Influence

```text

- Tell me about a time you led a project or team.
- Describe a situation where you had to influence without authority.
- How did you handle a situation where you disagreed with your manager?
- Tell me about a time you had to make a difficult decision with incomplete information.
- Describe a time you had to get buy-in from multiple stakeholders.

```

### Conflict & Collaboration

```text

- Tell me about a time you had a conflict with a coworker.
- Describe a situation where you had to work with someone difficult.
- How did you handle a disagreement about technical approach?
- Tell me about a time you had to give difficult feedback.
- Describe a time you had to collaborate across teams.

```

### Failure & Learning

```text

- Tell me about a time you failed.
- Describe a mistake you made and how you handled it.
- What's the biggest technical mistake you've made?
- How did you handle a project that was behind schedule?
- Tell me about a time you had to quickly learn something new.

```

### Technical Decisions

```text

- Describe a difficult technical decision you made.
- Tell me about a time you chose a technology that didn't work out.
- How did you handle technical debt in a project?
- Describe a time you had to balance speed vs quality.
- Tell me about a time you improved system performance.

```

### Customer Focus

```text

- Tell me about a time you went above and beyond for a customer.
- How did you handle conflicting customer requirements?
- Describe a time you used data to make a product decision.
- How did you prioritize features based on customer feedback?

```

## Story Bank Template

```text

Prepare 8-10 versatile stories that can answer multiple questions:

Story 1: Technical Leadership
- Led architecture migration
- Can answer: leadership, technical decisions, impact

Story 2: Conflict Resolution
- Disagreed with teammate on approach
- Can answer: conflict, collaboration, compromise

Story 3: Failure & Recovery
- Production outage I caused
- Can answer: failure, learning, process improvement

Story 4: Learning New Technology
- Quickly learned Kubernetes for a project
- Can answer: learning, adaptability, growth mindset

Story 5: Cross-Team Collaboration
- Worked with product, design, and backend teams
- Can answer: collaboration, communication, stakeholder management

Story 6: Customer Impact
- Improved performance that reduced churn
- Can answer: customer focus, impact, metrics

Story 7: Mentoring
- Helped junior engineer grow
- Can answer: leadership, mentoring, team development

Story 8: Process Improvement
- Introduced code review process
- Can answer: ownership, standards, improvement

Story 9: Ambiguity
- Built feature with unclear requirements
- Can answer: ambiguity, problem-solving, initiative

Story 10: Deadline Pressure
- Delivered critical feature under tight deadline
- Can answer: pressure, prioritization, delivery

```

## STAR Story Structure (2 minutes max)

```text

Opening (10 seconds):
"I'd like to talk about [situation]..."

Situation (15 seconds):
"In my role at [company], we were [context]..."

Task (10 seconds):
"My responsibility was [specific task]..."

Action (60-90 seconds):
"First, I [action 1]...
 Then, I [action 2]...
 Finally, I [action 3]..."

Result (15 seconds):
"As a result, [quantified outcome]...
 What I learned was [lesson]..."

```

### Resources for Behavioral Interviews

- 📘 **Book:** *Cracking the Coding Interview* — behavioral section
- 📘 **Book:** *The Amazon Way* by John Rossman — leadership principles
- 🌐 **Website:** [Amazon Leadership Principles](https://www.amazon.jobs/en/principles) — official
- 🌐 **Website:** [Exponent Behavioral Prep](https://www.tryexponent.com/courses/behavioral) — structured prep
- 🎥 **YouTube:**

---

# Phase 23: Resume Deep Dive

> **Why It Matters:** Your resume is your first impression. Every line must be defensible and demonstrate impact.

## Resume Format for SDE

```text

[Your Name]
[Email] | [Phone] | [LinkedIn] | [GitHub] | [Portfolio]

EXPERIENCE
[Company Name] — [Title]                     [Month Year – Present]
• [Achievement with metric]
• [Achievement with metric]
• [Achievement with metric]

EDUCATION
[University] — [Degree]                      [Month Year – Month Year]
• Relevant coursework, GPA (if > 3.5)

SKILLS
Languages: Java, TypeScript, Python, SQL
Frameworks: React, Next.js, NestJS, Spring Boot
Tools: Docker, Kubernetes, Kafka, Redis, PostgreSQL
Cloud: AWS, Azure, GCP

PROJECTS
[Project Name]                               [Month Year]
• [What it does]
• [Tech stack]
• [Impact/metric]

```

## Writing Impactful Bullet Points

```text

Formula: Action Verb + What You Did + Technology/Method + Impact/Metric

Good:
✅ "Reduced API response time by 60% by implementing Redis caching layer
    serving 10M daily requests"
✅ "Led migration from monolith to microservices architecture, improving
    deployment frequency from monthly to daily"
✅ "Designed and implemented real-time notification system using WebSocket
    and Kafka, handling 500K concurrent connections"

Bad:
❌ "Worked on backend services" (no action, no metric)
❌ "Responsible for API development" (passive, no impact)
❌ "Used React to build frontend" (no outcome)

```

## Project Descriptions

```text

Project: E-Commerce Platform
- Built full-stack e-commerce platform with React, Next.js, NestJS, and PostgreSQL
- Implemented payment processing with Stripe, handling 10K+ transactions/day
- Designed product search with Elasticsearch, reducing query time from 2s to 50ms
- Deployed on AWS with Docker/Kubernetes, achieving 99.9% uptime
- Tech: React, Next.js, NestJS, PostgreSQL, Redis, Elasticsearch, Docker, AWS

Project: Real-Time Chat Application
- Developed WebSocket-based chat application supporting 10K concurrent users
- Implemented message persistence with Cassandra and presence tracking with Redis
- Built notification system with Firebase Cloud Messaging for mobile push
- Tech: React, Node.js, WebSocket, Cassandra, Redis, Docker

```

## Common Resume Mistakes

```text

1. ❌ No metrics or quantifiable results
2. ❌ Passive language ("responsible for", "worked on")
3. ❌ Too long (keep to 1-2 pages)
4. ❌ Irrelevant information (hobbies, references)
5. ❌ Typos or grammatical errors
6. ❌ Generic descriptions that could apply to anyone
7. ❌ Missing tech stack details
8. ❌ No links to projects or GitHub

Best Practices:
✅ Tailor resume for each company/role
✅ Use keywords from job description
✅ Start each bullet with strong action verb
✅ Include 3-4 bullets per role
✅ Highlight leadership and impact
✅ Include side projects that show passion

```

## Action Verbs for Technical Resumes

```text

Architected, Built, Designed, Developed, Implemented, Led, Optimized,
Reduced, Increased, Improved, Automated, Migrated, Deployed, Launched,
Scaled, Integrated, Refactored, Streamlined, Mentored, Collaborated,
Delivered, Launched, Standardized, Established, Created, Established

```

### Resources for Resume

- 📘 **Book:** *Cracking the Coding Interview* — resume chapter
- 🌐 **Website:** [Resume Worded](https://resumeworded.com/) — AI resume review
- 🌐 **Website:** [Jake's Resume Template](https://www.overleaf.com/latex/templates/jakes-resume/syzfjbzcjxzx) — clean LaTeX template
- 🎥 **YouTube:** [NeetCode Resume Tips](https://www.youtube.com/@NeetCode)

---

# Phase 24: Testing

> **Why It Matters:** Testing is a critical skill that demonstrates code quality awareness. Interviewers often ask about testing strategies and may ask you to write tests during coding rounds.

## Testing Pyramid

```text

         /\
        /  \        E2E Tests (few, slow, expensive)
       / E2E\       - Test full user flows
      /------\
     /        \     Integration Tests (some, medium speed)
    / Integr.  \    - Test component interactions
   /------------\
  /              \  Unit Tests (many, fast, cheap)
 /   Unit Tests   \ - Test individual functions/classes
/------------------\

```

## Unit Testing with JUnit

```java
import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;

class CalculatorTest {

    private Calculator calculator;

    @BeforeEach
    void setUp() {
        calculator = new Calculator();
    }

    @Test
    void shouldAddTwoNumbers() {
        assertEquals(5, calculator.add(2, 3));
    }

    @Test
    void shouldSubtractTwoNumbers() {
        assertEquals(1, calculator.subtract(3, 2));
    }

    @Test
    void shouldDivideTwoNumbers() {
        assertEquals(2.5, calculator.divide(5, 2), 0.001);
    }

    @Test
    void shouldThrowExceptionWhenDividingByZero() {
        assertThrows(ArithmeticException.class,
            () -> calculator.divide(5, 0));
    }

    @ParameterizedTest
    @CsvSource({
        "1, 1, 2",
        "2, 3, 5",
        "10, 20, 30"
    })
    void shouldAddMultiplePairs(int a, int b, int expected) {
        assertEquals(expected, calculator.add(a, b));
    }

    @Test
    @DisplayName("Should handle negative numbers correctly")
    void shouldHandleNegativeNumbers() {
        assertEquals(-5, calculator.add(-2, -3));
    }
}

```

## Mocking with Mockito

```java
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import static org.mockito.Mockito.*;
import static org.junit.jupiter.api.Assertions.*;

@ExtendWith(MockitoExtension.class)
class OrderServiceTest {

    @Mock
    private OrderRepository orderRepository;

    @Mock
    private PaymentService paymentService;

    @Mock
    private NotificationService notificationService;

    @InjectMocks
    private OrderService orderService;

    @Test
    void shouldCreateOrderSuccessfully() {
        // Arrange
        OrderRequest request = new OrderRequest("product-1", 2);
        when(orderRepository.save(any(Order.class)))
            .thenReturn(new Order(1L, "product-1", 2, OrderStatus.PENDING));
        when(paymentService.processPayment(anyDouble()))
            .thenReturn(true);

        // Act
        Order order = orderService.createOrder(request);

        // Assert
        assertNotNull(order);
        assertEquals(OrderStatus.CONFIRMED, order.getStatus());

        verify(orderRepository).save(any(Order.class));
        verify(paymentService).processPayment(anyDouble());
        verify(notificationService).sendConfirmation(any(Order.class));
    }

    @Test
    void shouldFailWhenPaymentFails() {
        // Arrange
        when(orderRepository.save(any(Order.class)))
            .thenReturn(new Order(1L, "product-1", 2, OrderStatus.PENDING));
        when(paymentService.processPayment(anyDouble()))
            .thenReturn(false);

        // Act
        Order order = orderService.createOrder(new OrderRequest("product-1", 2));

        // Assert
        assertEquals(OrderStatus.FAILED, order.getStatus());
        verify(notificationService).sendFailure(any(Order.class));
    }

    @Test
    void shouldGetOrderById() {
        // Arrange
        when(orderRepository.findById(1L))
            .thenReturn(Optional.of(new Order(1L, "product-1", 2, OrderStatus.PENDING)));

        // Act
        Order order = orderService.getOrder(1L);

        // Assert
        assertNotNull(order);
        assertEquals("product-1", order.getProductId());
    }

    @Test
    void shouldThrowExceptionWhenOrderNotFound() {
        // Arrange
        when(orderRepository.findById(999L))
            .thenReturn(Optional.empty());

        // Act & Assert
        assertThrows(OrderNotFoundException.class,
            () -> orderService.getOrder(999L));
    }
}

```

## Integration Testing

```java
@SpringBootTest
@Transactional
class UserRepositoryIntegrationTest {

    @Autowired
    private UserRepository userRepository;

    @Test
    void shouldSaveAndRetrieveUser() {
        // Arrange
        User user = new User("Alice", "alice@example.com");

        // Act
        User saved = userRepository.save(user);
        Optional<User> found = userRepository.findById(saved.getId());

        // Assert
        assertTrue(found.isPresent());
        assertEquals("Alice", found.get().getName());
        assertEquals("alice@example.com", found.get().getEmail());
    }

    @Test
    void shouldFindUsersByEmail() {
        // Arrange
        userRepository.save(new User("Alice", "alice@example.com"));
        userRepository.save(new User("Bob", "bob@example.com"));

        // Act
        List<User> users = userRepository.findByEmailContaining("alice");

        // Assert
        assertEquals(1, users.size());
        assertEquals("Alice", users.get(0).getName());
    }
}

```

## API Testing

```java
@SpringBootTest(webEnvironment = WebEnvironment.RANDOM_PORT)
class UserControllerTest {

    @Autowired
    private TestRestTemplate restTemplate;

    @Test
    void shouldCreateUser() {
        CreateUserRequest request = new CreateUserRequest("Alice", "alice@example.com");

        ResponseEntity<User> response = restTemplate.postForEntity(
            "/api/users", request, User.class);

        assertEquals(HttpStatus.CREATED, response.getStatusCode());
        assertNotNull(response.getBody());
        assertEquals("Alice", response.getBody().getName());
    }

    @Test
    void shouldReturn404ForNonexistentUser() {
        ResponseEntity<User> response = restTemplate.getForEntity(
            "/api/users/999", User.class);

        assertEquals(HttpStatus.NOT_FOUND, response.getStatusCode());
    }
}

```

## Testing Best Practices

```text

Unit Tests:
✅ Test one thing at a time
✅ Use descriptive test names
✅ Follow AAA pattern (Arrange, Act, Assert)
✅ Mock external dependencies
✅ Test edge cases and error scenarios
✅ Keep tests fast (< 100ms each)

Integration Tests:
✅ Test component interactions
✅ Use test database (not production)
✅ Clean up after tests
✅ Test happy path and error paths

E2E Tests:
✅ Test critical user flows
✅ Use real (or realistic) data
✅ Keep number small (expensive to run)
✅ Run in CI/CD pipeline

General:
✅ Aim for 80%+ code coverage
✅ Don't test framework code
✅ Test behavior, not implementation
✅ Write tests before fixing bugs (regression tests)
✅ Use test data builders/factories

```

## Test Data Builders

```java
// Builder pattern for test data
public class UserBuilder {
    private String name = "Test User";
    private String email = "test@example.com";
    private int age = 25;
    private boolean active = true;

    public UserBuilder withName(String name) { this.name = name; return this; }
    public UserBuilder withEmail(String email) { this.email = email; return this; }
    public UserBuilder withAge(int age) { this.age = age; return this; }
    public UserBuilder inactive() { this.active = false; return this; }

    public User build() {
        return new User(name, email, age, active);
    }
}

// Usage in tests
User user = new UserBuilder()
    .withName("Alice")
    .withEmail("alice@example.com")
    .build();

```

### Resources for Testing

- 📘 **Book:** *Clean Code* by Robert Martin — testing chapter
- 📘 **Book:** *xUnit Test Patterns* by Gerard Meszaros — testing patterns
- 🌐 **Website:** [JUnit 5 Documentation](https://junit.org/junit5/docs/current/user-guide/)
- 🌐 **Website:** [Mockito Documentation](https://site.mockito.org/)
- 🌐 **Website:** [Test Driven Development](https://martinfowler.com/bliki/TestDrivenDevelopment.html) — Martin Fowler

---

# Phase 25: Cloud & Infrastructure

> **Why It Matters:** Cloud knowledge is essential for modern system design. Understanding containers, orchestration, and CI/CD demonstrates production readiness.

## Docker

```dockerfile
# Dockerfile
FROM openjdk:17-slim
WORKDIR /app
COPY target/*.jar app.jar
EXPOSE 8080
ENTRYPOINT ["java", "-jar", "app.jar"]

```

```bash
# Docker commands
docker build -t myapp:1.0 .           # Build image
docker run -p 8080:8080 myapp:1.0     # Run container
docker ps                              # List running containers
docker logs <container>                # View logs
docker exec -it <container> bash       # Shell into container
docker-compose up -d                   # Start services
docker-compose down                    # Stop services

```

## Docker Compose

```yaml
version: '3.8'
services:
  app:
    build: .
    ports:
      - "8080:8080"
    environment:
      - DATABASE_URL=postgresql://db:5432/mydb
    depends_on:
      - db
      - redis

  db:
    image: postgres:15
    environment:
      - POSTGRES_DB=mydb
      - POSTGRES_PASSWORD=secret
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine

  kafka:
    image: confluentinc/cp-kafka:7.4.0
    environment:
      KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://kafka:9092

volumes:
  postgres_data:

```

## Kubernetes Basics

```yaml
# Deployment
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
    spec:
      containers:
      - name: myapp
        image: myapp:1.0
        ports:
        - containerPort: 8080
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 30
          periodSeconds: 10

---
# Service
apiVersion: v1
kind: Service
metadata:
  name: myapp-service
spec:
  selector:
    app: myapp
  ports:
  - port: 80
    targetPort: 8080
  type: LoadBalancer

---
# Horizontal Pod Autoscaler
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: myapp-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: myapp
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70

```

## CI/CD with GitHub Actions

```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Set up JDK 17
      uses: actions/setup-java@v3
      with:
        java-version: '17'
        distribution: 'temurin'
    - name: Build and Test
      run: mvn clean test
    - name: Upload Coverage
      uses: codecov/codecov-action@v3

  deploy:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
    - uses: actions/checkout@v3
    - name: Build Docker Image
      run: docker build -t myapp:${{ github.sha }} .
    - name: Push to ECR
      run: |
        aws ecr get-login-password | docker login --username AWS --password-stdin $ECR_URL
        docker tag myapp:${{ github.sha }} $ECR_URL/myapp:${{ github.sha }}
        docker push $ECR_URL/myapp:${{ github.sha }}
    - name: Deploy to EKS
      run: |
        kubectl set image deployment/myapp myapp=$ECR_URL/myapp:${{ github.sha }}

```

## AWS Services You Should Know

```text

Compute:
├── EC2 — virtual machines
├── Lambda — serverless functions
├── ECS/EKS — container orchestration
└── Elastic Beanstalk — PaaS

Storage:
├── S3 — object storage
├── EBS — block storage
└── EFS — file storage

Database:
├── RDS — managed relational (PostgreSQL, MySQL)
├── DynamoDB — managed NoSQL
├── ElastiCache — managed Redis/Memcached
└── Aurora — serverless relational

Messaging:
├── SQS — simple queue service
├── SNS — notification service
├── Kinesis — real-time streaming
└── EventBridge — event bus

Security:
├── IAM — identity and access management
├── KMS — key management
├── Cognito — user authentication
└── WAF — web application firewall

CDN & DNS:
├── CloudFront — CDN
├── Route 53 — DNS
└── API Gateway — managed API

Monitoring:
├── CloudWatch — monitoring and logs
├── X-Ray — distributed tracing
└── CloudTrail — audit logging

```

## Azure Services (Microsoft)

```text

Compute:
├── Azure VMs — virtual machines
├── Azure Functions — serverless
├── Azure Kubernetes Service (AKS) — container orchestration
└── App Service — PaaS

Storage:
├── Blob Storage — object storage
├── Disk Storage — block storage
└── File Storage — file shares

Database:
├── Azure SQL — managed SQL Server
├── Cosmos DB — globally distributed NoSQL
├── Azure Database for PostgreSQL
└── Azure Cache for Redis

Messaging:
├── Service Bus — enterprise messaging
├── Event Hubs — real-time streaming
├── Event Grid — event routing
└── Queue Storage — simple queues

Security:
├── Azure AD — identity management
├── Key Vault — secrets management
└── Sentinel — security analytics

CDN & DNS:
├── Azure CDN — content delivery
├── Azure DNS — DNS management
└── API Management — managed APIs

```

### Resources for Cloud & Infrastructure

- 📘 **Book:** *Docker Deep Dive* by Nigel Poulton
- 📘 **Book:** *Kubernetes in Action* by Marko Lukša
- 🌐 **Website:** [Docker Documentation](https://docs.docker.com/)
- 🌐 **Website:** [Kubernetes Documentation](https://kubernetes.io/docs/)
- 🌐 **Website:** [AWS Well-Architected Framework](https://aws.amazon.com/architecture/well-architected/)
- 🌐 **Website:** [Azure Architecture Center](https://learn.microsoft.com/en-us/azure/architecture/)
- 🎥 **YouTube:** [TechWorld with Nana](https://www.youtube.com/@TechWorldwithNana) — Docker & K8s
- 🌐 **Website:** [Play with Docker](https://labs.play-with-docker.com/) — free Docker playground
- 🌐 **Website:** [KillerCoda](https://killercoda.com/) — interactive Kubernetes scenarios

---

# Phase 26: Frontend (Full-Stack)

> **Why It Matters:** As a full-stack developer, you need deep frontend knowledge. React, performance optimization, and browser internals are common interview topics.

## JavaScript Internals

### Event Loop

```text

Call Stack: Executes synchronous code
Web APIs: Browser APIs (setTimeout, fetch, DOM)
Callback Queue: Async callbacks waiting to execute
Microtask Queue: Promises, queueMicrotask (higher priority)

Execution Order:
1. Call stack (synchronous)
2. Microtask queue (promises)
3. Macrotask queue (setTimeout, setInterval)

console.log('1');                    // sync
setTimeout(() => console.log('2'), 0); // macrotask
Promise.resolve().then(() => console.log('3')); // microtask
console.log('4');                    // sync

Output: 1, 4, 3, 2

```

### Closures

```javascript
function createCounter() {
    let count = 0; // enclosed variable

    return {
        increment: () => ++count,
        decrement: () => --count,
        getCount: () => count
    };
}

const counter = createCounter();
counter.increment(); // 1
counter.increment(); // 2
counter.getCount();  // 2

```

### Prototypal Inheritance

```javascript
function Animal(name) {
    this.name = name;
}

Animal.prototype.speak = function() {
    return `${this.name} makes a sound`;
};

function Dog(name) {
    Animal.call(this, name); // call parent constructor
}

Dog.prototype = Object.create(Animal.prototype);
Dog.prototype.constructor = Dog;

Dog.prototype.speak = function() {
    return `${this.name} barks`;
};

const dog = new Dog('Rex');
dog.speak(); // "Rex barks"

```

## TypeScript Advanced Types

```typescript
// Utility Types
type Partial<T> = { [P in keyof T]?: T[P] };
type Required<T> = { [P in keyof T]-?: T[P] };
type Readonly<T> = { readonly [P in keyof T]: T[P] };
type Pick<T, K extends keyof T> = { [P in K]: T[P] };
type Omit<T, K extends keyof T> = Pick<T, Exclude<keyof T, K>>;
type Record<K extends keyof T, T> = { [P in K]: T[P] };

// Conditional Types
type IsString<T> = T extends string ? true : false;
type A = IsString<'hello'>; // true
type B = IsString<42>;      // false

// Mapped Types
type Optional<T> = {
    [K in keyof T]?: T[K]
};

// Template Literal Types
type EventName = `on${Capitalize<'click' | 'hover'>}`;
// 'onClick' | 'onHover'

// Infer
type ReturnType<T> = T extends (...args: any[]) => infer R ? R : never;
type ParamType<T> = T extends (...args: infer P) => any ? P : never;

// Discriminated Unions
type Shape =
    | { kind: 'circle'; radius: number }
    | { kind: 'rectangle'; width: number; height: number }
    | { kind: 'triangle'; base: number; height: number };

function area(shape: Shape): number {
    switch (shape.kind) {
        case 'circle': return Math.PI * shape.radius ** 2;
        case 'rectangle': return shape.width * shape.height;
        case 'triangle': return (shape.base * shape.height) / 2;
    }
}

```

## React Hooks Deep Dive

```typescript
// useState
const [count, setCount] = useState(0);
const increment = () => setCount(prev => prev + 1); // functional update

// useEffect
useEffect(() => {
    const subscription = api.subscribe(data);
    return () => subscription.unsubscribe(); // cleanup
}, [data]); // dependency array

// useRef
const inputRef = useRef<HTMLInputElement>(null);
useEffect(() => inputRef.current?.focus(), []);

// useMemo (memoize expensive calculations)
const filteredItems = useMemo(() => {
    return items.filter(item => item.match(searchTerm));
}, [items, searchTerm]);

// useCallback (memoize function reference)
const handleSubmit = useCallback((data: FormData) => {
    submitData(data);
}, [submitData]);

// useReducer (complex state logic)
function reducer(state: State, action: Action): State {
    switch (action.type) {
        case 'increment': return { count: state.count + 1 };
        case 'decrement': return { count: state.count - 1 };
        default: throw new Error('Unknown action');
    }
}

// Custom Hook
function useLocalStorage<T>(key: string, initialValue: T) {
    const [storedValue, setStoredValue] = useState<T>(() => {
        try {
            const item = window.localStorage.getItem(key);
            return item ? JSON.parse(item) : initialValue;
        } catch {
            return initialValue;
        }
    });

    const setValue = (value: T | ((val: T) => T)) => {
        const valueToStore = value instanceof Function ? value(storedValue) : value;
        setStoredValue(valueToStore);
        window.localStorage.setItem(key, JSON.stringify(valueToStore));
    };

    return [storedValue, setValue] as const;
}

```

## React Performance Optimization

```typescript
// 1. Memoize expensive components
const ExpensiveList = React.memo(({ items }: { items: Item[] }) => {
    return items.map(item => <ExpensiveItem key={item.id} item={item} />);
});

// 2. Virtualize large lists
import { useVirtualizer } from '@tanstack/react-virtual';

function VirtualList({ items }: { items: Item[] }) {
    const parentRef = useRef<HTMLDivElement>(null);
    const virtualizer = useVirtualizer({
        count: items.length,
        getScrollElement: () => parentRef.current,
        estimateSize: () => 35,
    });

    return (
        <div ref={parentRef} style={{ height: '400px', overflow: 'auto' }}>
            <div style={{ height: virtualizer.getTotalSize() }}>
                {virtualizer.getVirtualItems().map(virtualRow => (
                    <div key={virtualRow.key}
                         style={{
                             position: 'absolute',
                             top: virtualRow.start,
                             height: virtualRow.size,
                         }}>
                        {items[virtualRow.index].name}
                    </div>
                ))}
            </div>
        </div>
    );
}

// 3. Code splitting
const Dashboard = lazy(() => import('./Dashboard'));
const Settings = lazy(() => import('./Settings'));

// 4. Avoid unnecessary re-renders
// Use React DevTools Profiler to identify bottlenecks

// 5. Optimize images
<img src="photo.webp" loading="lazy" alt="Photo" />

```

## Next.js App Router

```typescript
// app/layout.tsx — root layout
export default function RootLayout({ children }) {
    return (
        <html lang="en">
            <body>{children}</body>
        </html>
    );
}

// app/page.tsx — Server Component by default
async function HomePage() {
    const data = await fetch('https://api.example.com/data');
    const posts = await data.json();

    return (
        <main>
            <h1>Welcome</h1>
            {posts.map(post => <PostCard key={post.id} post={post} />)}
        </main>
    );
}

// app/posts/[id]/page.tsx — Dynamic route
async function PostPage({ params }: { params: { id: string } }) {
    const post = await getPost(params.id);
    return <Post post={post} />;
}

// Client Component
'use client';
import { useState } from 'react';

function Counter() {
    const [count, setCount] = useState(0);
    return <button onClick={() => setCount(c => c + 1)}>Count: {count}</button>;
}

```

## Browser Rendering Pipeline

```text

1. DOM Construction — HTML → DOM tree
2. CSSOM Construction — CSS → CSSOM tree
3. Render Tree — DOM + CSSOM
4. Layout — Calculate positions and sizes
5. Paint — Fill in pixels
6. Compositing — Combine layers

Optimization Tips:
- Minimize DOM depth
- Avoid layout thrashing (read then write)
- Use transform and opacity for animations (compositor-only)
- Use will-change for animations
- Debounce scroll/resize handlers

```

### Resources for Frontend

- 📘 **Book:** *You Don't Know JS* by Kyle Simpson — JavaScript deep dive
- 📘 **Book:** *Eloquent JavaScript* by Marijn Haverbeke
- 📘 **Book:** *Learning React* by Eve Porcello
- 🌐 **Website:** [React Documentation](https://react.dev/)
- 🌐 **Website:** [Next.js Documentation](https://nextjs.org/docs)
- 🌐 **Website:** [TypeScript Handbook](https://www.typescriptlang.org/docs/handbook/)
- 🌐 **Website:** [javascript.info](https://javascript.info/) — modern JS tutorial
- 🎥 **YouTube:** [Fireship](https://www.youtube.com/@Fireship) — quick frontend concepts
- 🌐 **Website:** [web.dev](https://web.dev/) — web performance best practices

---

# Phase 27: Mock Interviews & Practice

> **Why It Matters:** Practice is the most important part of interview preparation. You need to simulate real interview conditions to build confidence and identify weak areas.

## Practice Schedule

```text

Week 1-4: Foundation
- Solve 3-5 easy problems daily (patterns)
- Read system design book (1 chapter/day)
- Practice 1 behavioral story daily

Week 5-8: Intensity
- Solve 3-4 medium problems daily
- Complete 1 system design problem daily
- Do 1 mock behavioral interview weekly

Week 9-12: Polish
- Solve 2-3 medium/hard problems daily
- Complete 2 system design problems daily
- Do 2 mock interviews weekly (coding + system design)

Week 13-16: Final Prep
- Review weak areas
- Full mock interviews (2-3 hours each)
- Company-specific preparation

```

## Mock Interview Platforms

```text

Free:
├── [Pramp](https://www.pramp.com/) — peer-to-peer mock interviews
├── [Interviewing.io](https://interviewing.io/) — anonymous mock interviews
└── [LeetCode Discuss](https://leetcode.com/discuss/) — community solutions

Paid:
├── [Exponent](https://www.tryexponent.com/) — structured prep + mock interviews
├── [IGotAnOffer](https://igotanoffer.com/) — 1-on-1 with ex-FAANG
├── [Educative.io](https://educative.io/) — interactive courses
└── [AlgoExpert](https://www.algoexpert.io/) — curated problems + videos

Self-Practice:
├── Timer: 20-25 min for medium, 35-45 min for hard
├── Talk out loud (practice explaining)
├── Write on paper/whiteboard
└── Record yourself and review

```

## Interview Day Tips

```text

Before Interview:
✅ Test your setup (camera, mic, internet)
✅ Have water and notepad ready
✅ Review company's recent news/products
✅ Prepare questions to ask interviewer

During Coding Interview:
✅ Clarify requirements before coding
✅ Discuss brute force first, then optimize
✅ Think out loud — explain your thought process
✅ Ask about edge cases
✅ Test your solution with examples
✅ Analyze time/space complexity

During System Design:
✅ Ask clarifying questions (requirements, constraints)
✅ Start with high-level design
✅ Deep dive into components
✅ Discuss trade-offs
✅ Address bottlenecks and scaling

During Behavioral:
✅ Use STAR method
✅ Be specific with examples
✅ Quantify impact when possible
✅ Show growth mindset
✅ Be honest about failures

After Interview:
✅ Send thank you email within 24 hours
✅ Note what went well and what to improve
✅ Don't overthink — move to next preparation

```

---

# Phase 28: Company-Specific Preparation

> **Why It Matters:** Each company has unique interview styles, values, and focus areas. Tailoring your preparation to specific companies significantly increases your chances.

## Microsoft

```text

Focus Areas:
├── Coding: Arrays, Strings, Trees, Graphs, DP
├── System Design: Large-scale distributed systems, Azure
├── Behavioral: Growth mindset, collaboration, learning from failure
├── Culture: Empathy, inclusion, customer obsession

Tips:
- Know Microsoft's products (Azure, Teams, Office 365, GitHub)
- Emphasize learning from failure
- Show how you help others grow
- Mention cross-team collaboration

Common Questions:
- Design a file synchronization system (OneDrive-like)
- Design a notification system (Teams-like)
- Design a document collaboration system

```

## Google

```text

Focus Areas:
├── Coding: Heavy algorithmic focus, DP, Graphs
├── System Design: Large-scale, distributed, Google-scale
├── Behavioral: Googleyness, leadership, ambiguity
├── Culture: Innovation, impact, collaboration

Tips:
- Expect very hard coding questions
- Focus on scalability in system design
- Show intellectual curiosity
- Demonstrate ability to handle ambiguity

Common Questions:
- Design Google Search Autocomplete
- Design YouTube/Netflix
- Design Google Maps

```

## Amazon

```text

Focus Areas:
├── Coding: Arrays, Strings, Trees, Graphs
├── System Design: E-commerce, logistics, scale
├── Behavioral: ALL 16 Leadership Principles
├── Culture: Customer obsession, ownership, bias for action

Tips:
- Prepare stories for every leadership principle
- Quantify impact in every story
- Show customer obsession
- Demonstrate ownership and accountability

Common Questions:
- Design a payment system
- Design an e-commerce platform
- Design a recommendation engine

```

## Meta (Facebook)

```text

Focus Areas:
├── Coding: Arrays, Strings, Trees, Graphs, DP
├── System Design: Social graph, news feed, real-time
├── Behavioral: Impact, move fast, build social value
├── Culture: Boldness, transparency, community

Tips:
- Know Meta's products (Facebook, Instagram, WhatsApp, Messenger)
- Focus on social features in system design
- Show bias for action
- Demonstrate impact at scale

Common Questions:
- Design News Feed
- Design Facebook Messenger/WhatsApp
- Design Instagram Stories

```

## Apple

```text

Focus Areas:
├── Coding: Strong fundamentals, attention to detail
├── System Design: Privacy-focused, hardware-software integration
├── Behavioral: Excellence, innovation, collaboration
├── Culture: Secrecy, quality, user experience

Tips:
- Show attention to detail and polish
- Emphasize user experience
- Demonstrate ability to work in secrecy
- Show passion for Apple products

Common Questions:
- Design iMessage
- Design AirDrop
- Design HealthKit

```

## Netflix

```text

Focus Areas:
├── Coding: Strong fundamentals, practical solutions
├── System Design: Streaming, CDN, personalization
├── Behavioral: Freedom and responsibility, judgment
├── Culture: High performance, innovation

Tips:
- Know Netflix's tech stack (AWS, Java, microservices)
- Focus on streaming and content delivery
- Show freedom and responsibility mindset
- Demonstrate high performance culture

Common Questions:
- Design video streaming system
- Design recommendation engine
- Design content delivery network

```

## Interview Preparation Checklist

```text

2 Weeks Before:
✅ Resume polished and reviewed
✅ LinkedIn updated
✅ GitHub profile cleaned up
✅ Practice problems completed (100+ medium, 30+ hard)
✅ System design practice completed (10+ problems)
✅ Behavioral stories prepared (10+ stories)
✅ Mock interviews done (5+)

1 Week Before:
✅ Company research completed
✅ Recent news about company reviewed
✅ Questions to ask interviewer prepared
✅ Technical setup tested
✅ Relax and rest

Day Before:
✅ Review key concepts
✅ Review company-specific preparation
✅ Prepare interview outfit
✅ Set up workspace
✅ Get good sleep

Day Of:
✅ Eat healthy breakfast
✅ Arrive/log in early
✅ Stay calm and confident
✅ Be yourself
✅ Ask good questions

```

---

# Final Summary

## The Complete Interview Prep Roadmap

```text

Phase 1:   Java Language Mastery          — 25 hours
Phase 2:   Time & Space Complexity        — 10 hours
Phase 3:   Data Structures                — 40 hours
Phase 4:   Algorithms                     — 30 hours
Phase 5:   Pattern Recognition            — 60 hours
Phase 6:   Dynamic Programming            — 40 hours
Phase 7:   Graph Algorithms               — 30 hours
Phase 8:   Trees                          — 25 hours
Phase 9:   Bit Manipulation               — 10 hours
Phase 10:  Mathematics                    — 15 hours
Phase 11:  OOP                            — 25 hours
Phase 12:  Design Patterns                — 25 hours
Phase 13:  Operating Systems              — 20 hours
Phase 14:  Computer Networks              — 20 hours
Phase 15:  Databases                      — 25 hours
Phase 16:  System Design                  — 60 hours
Phase 17:  REST APIs                      — 15 hours
Phase 18:  Security                       — 15 hours
Phase 19:  Concurrency                    — 20 hours
Phase 20:  Git & Version Control          — 10 hours
Phase 21:  Linux & Shell                  — 10 hours
Phase 22:  Behavioral Interviews          — 20 hours
Phase 23:  Resume Deep Dive               — 10 hours
Phase 24:  Testing                        — 15 hours
Phase 25:  Cloud & Infrastructure         — 15 hours
Phase 26:  Frontend (Full-Stack)          — 20 hours
Phase 27:  Mock Interviews & Practice     — 40 hours
Phase 28:  Company-Specific Preparation   — 15 hours

Total: ~640 hours (~16 weeks at 40 hrs/week)

```

## Key Success Factors

```text

1. Consistency > Intensity
   - Study daily, even if just 1-2 hours
   - Avoid cramming before interviews

2. Quality > Quantity
   - Understand patterns, not just solutions
   - Explain solutions out loud

3. Practice > Reading
   - Code every day
   - Do mock interviews regularly

4. Feedback > Isolation
   - Get mock interview feedback
   - Join study groups

5. Mental Health
   - Take breaks
   - Exercise regularly
   - Sleep well
   - Stay positive

```

## Recommended Study Plan

```text

If you have 3 months (12 weeks):
- Weeks 1-4: Java, DSA fundamentals, easy/medium problems
- Weeks 5-8: System design, advanced DSA, medium/hard problems
- Weeks 9-12: Mock interviews, company-specific prep, review

If you have 6 months (24 weeks):
- Weeks 1-8: Foundation (all topics at basic level)
- Weeks 9-16: Intermediate (deep dive into each topic)
- Weeks 17-24: Advanced (mock interviews, company prep)

```

## Best Resources Summary

```text

Books:
📘 Cracking the Coding Interview — Gayle McDowell
📘 Elements of Programming Interviews — Adnan Aziz
📘 System Design Interview (Vol 1 & 2) — Alex Xu
📘 Designing Data-Intensive Applications — Martin Kleppmann
📘 Effective Java — Joshua Bloch
📘 Java Concurrency in Practice — Brian Goetz

Websites:
🌐 LeetCode — practice problems
🌐 NeetCode.io — pattern-based learning
🌐 System Design Primer — GitHub resource
🌐 Refactoring.Guru — design patterns
🌐 Use The Index, Luke — SQL indexing
🌐 MDN Web Docs — web technologies

YouTube:
🎥 NeetCode — problem explanations
🎥 take U forward — DSA series
🎥 ByteByteGo — system design
🎥 Hello Interview — structured prep
🎥 Fireship — quick tech concepts
🎥 Amigoscode — Java & design patterns

Courses:
💻 Educative.io — interactive courses
💻 AlgoExpert — curated problems
💻 Exponent — system design + mock interviews

```

---

> **Remember:** Getting a job at a top product-based company is a marathon, not a sprint. Stay consistent, stay positive, and trust the process. You've got this! 🚀

---

## 🔗 Related Files

| File | Description |
|------|-------------|
| [Complete Guide](01-Complete-Guide.md) | Phases 1-8: Java, DSA, Algorithms |
| [Core CS Fundamentals](02-Core-CS-Fundamentals.md) | Phases 9-16: CS Fundamentals, NoSQL |
| [System Design & APIs](03-System-Design-APIs-Security.md) | Phases 17-20: System Design, REST, Security |
| [Advanced Topics](05-Advanced-Topics.md) | Segment Tree, DI, Repository, MVC |
| [LeetCode Study Plan](06-LeetCode-Study-Plan.md) | 12-week intensive study plan |
| [Cheat Sheet](07-Cheat-Sheet.md) | Last-minute review for all 28 phases |
| [Microsoft Guide](16-Microsoft-Azure-Interview-Guide.md) | Microsoft Azure team-specific prep |
| [Progress Tracker](08-Progress-Tracker.md) | Track your weekly progress |
| [Mock Interview Bank](09-Mock-Interview-Question-Bank.md) | 90 questions (Coding + SD + Behavioral) |
| [Google Guide](17-Google-Interview-Guide.md) | Google-specific interview prep |
| [Amazon Guide](18-Amazon-Interview-Guide.md) | Amazon Leadership Principles prep |
| [Meta Guide](19-Meta-Interview-Guide.md) | Meta-specific interview prep |
| [Apple Guide](20-Apple-Interview-Guide.md) | Apple-specific interview prep |
---

## Summary

This guide covers DevOps practices, behavioral interview preparation, and career growth strategies. Topics include CI/CD pipelines, containerization, monitoring, the STAR method, and navigating the senior engineering career path.

## See Also
- [Behavioral](../18-Behavioral/)
- [Coding Patterns](../19-Coding-Patterns/)
- [JavaScript](../01-JavaScript/)
- [React](../03-React/)
- [System Design](../11-System-Design/)
- [TypeScript](../02-TypeScript/)

## References & Learn More

- [LeetCode](https://leetcode.com/)
- [NeetCode](https://neetcode.io/)
- [System Design Primer](https://github.com/donnemartin/system-design-primer)
- [Levels.fyi](https://www.levels.fyi/)
- [Cracking the Coding Interview](http://www.crackingthecodinginterview.com/)
