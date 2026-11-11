# IS601 Module 10 Reflection

In Module 10, I continued building on my FastAPI and PostgreSQL calculator project from Module 9. This assignment helped me understand how user information can be stored more securely and how automated testing and deployment work together. I added a SQLAlchemy user model, Pydantic schemas to validate user information, and password hashing so that passwords are not stored as plain text.

One of my first challenges was getting my new user model to work with my existing PostgreSQL database. I kept receiving an internal server error when I tried to create a user. After looking at the application logs, I found that the original `users` table from Module 9 did not have a `password_hash` column. I solved that problem by using a separate `secure_users` table instead of deleting my previous work. When I tested the endpoint again, I finally received a successful `201 Created` response.

Testing was another challenge. At first, pytest reported that no tests had run. I learned that Docker needed to copy the test files into the application image. I also had to fix an accidental character in one of my test files. After those corrections, all eight unit and integration tests passed locally.

The most frustrating part was the GitHub Actions security scan. My workflow kept failing because Trivy reported vulnerabilities in Python packaging-related components. I tried several Dockerfile changes before finding a setup that passed the security scan. After that, deployment failed because GitHub did not have my Docker Hub credentials. I learned how to create a Docker Hub access token, store it in GitHub Actions secrets, and configure the corresponding username variable. The workflow finally completed successfully, and my image was pushed to Docker Hub.

This assignment was challenging and took much longer than I expected, but it taught me to read error messages carefully and solve one issue at a time. I now have more experience with secure Python application development, PostgreSQL, Docker, automated tests, GitHub Actions, and deployment. These are skills I can use in future projects and show in my GitHub portfolio.
