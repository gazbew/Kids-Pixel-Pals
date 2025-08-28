# Docker Development Setup

This setup provides a complete development environment for Kids Pixel Pals using Docker Compose.

## Services Included

- **PostgreSQL 15**: Primary database for the application
- **Redis 7**: Caching and pub/sub functionality
- **FastAPI**: Backend API service with hot reload

## Quick Start

1. **Install Docker**: Ensure Docker Desktop is installed and running
2. **Start Services**: Run the development startup script:
   ```bash
   ./start-dev.sh
   ```

3. **Access Services**:
   - API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs
   - PostgreSQL: localhost:5432
   - Redis: localhost:6379

## Manual Setup

If you prefer to run commands manually:

```bash
# Build and start containers
docker-compose up --build -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Stop and remove volumes
docker-compose down -v
```

## Environment Variables

Copy the example environment file and customize it:

```bash
cp .env.example .env
```

Update the `.env` file with your specific configuration:

- `DATABASE_URL`: PostgreSQL connection string
- `REDIS_URL`: Redis connection string
- `JWT_SECRET_KEY`: Secure random key for JWT signing
- `ENCRYPTION_KEY`: 32-byte key for AES-256 encryption
- `CORS_ORIGINS`: Allowed frontend origins

## Database Management

### Access PostgreSQL
```bash
docker exec -it kids-pixel-pals-postgres psql -U postgres -d kids_pixel_pals
```

### Run Migrations
Migrations are automatically applied when the API service starts.

### Reset Database
```bash
docker-compose down -v
docker-compose up -d
```

## Development Workflow

1. **Code Changes**: The backend code is mounted as a volume, so changes are reflected immediately
2. **Hot Reload**: FastAPI automatically reloads on code changes
3. **Database Changes**: Use Alembic migrations for schema changes
4. **Testing**: Run tests inside the container or locally

## Production Considerations

For production deployment:

1. Use proper secrets management
2. Set `DEBUG=false` and `ENVIRONMENT=production`
3. Use secure random keys for JWT and encryption
4. Configure proper CORS origins
5. Set up database backups
6. Use Docker Compose production configuration

## Troubleshooting

### Port Conflicts
If ports 5432, 6379, or 8000 are already in use, update the port mappings in `docker-compose.yml`.

### Build Issues
If you encounter build issues, try rebuilding from scratch:

```bash
docker-compose build --no-cache
```

### Database Connection Issues
Check if the database is healthy:

```bash
docker-compose logs postgres
```

### Redis Connection Issues
```bash
docker-compose logs redis
```