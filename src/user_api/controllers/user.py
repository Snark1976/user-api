from litestar import Controller, get, post, put, delete
from litestar.exceptions import HTTPException
from litestar.params import Parameter, Body
from uuid import UUID
from advanced_alchemy.extensions.litestar import (
    filters,
    providers,
    repository,
    service,
)
from src.user_api.models.user import User
from src.user_api.schemas.user import UserDTO, UserCreateDTO, UserUpdateDTO

class UserService(service.SQLAlchemyAsyncRepositoryService[User]):
    """User repository service."""

    class Repo(repository.SQLAlchemyAsyncRepository[User]):
        """User repository."""
        model_type = User

    repository_type = Repo

class UserController(Controller):
    path = "/users"
    dependencies = providers.create_service_dependencies(
        UserService,
        "users_service",
        filters={"pagination_type": "limit_offset", "id_filter": UUID, "search": "name", "search_ignore_case": True},
    )

    @get(
        description="Retrieve a list of all users with optional filtering."
    )
    async def list_users(
            self,
            users_service: UserService,
            limit: int = Parameter(query="limit", default=10, ge=1, le=100, description="Number of users to return."),
            offset: int = Parameter(query="offset", default=0, ge=0, description="Offset for pagination."),
            name: str | None = Parameter(query="name", default=None, description="Filter users by name (case-insensitive)."),
            surname: str | None = Parameter(query="surname", default=None, description="Filter users by surname (case-insensitive)."),
    ) -> list[UserDTO]:
        """List all users.

        Args:
            users_service: The user service to handle database operations.
            limit: Number of users to return (pagination).
            offset: Offset for pagination.
            name: Optional filter by user name (case-insensitive).
            surname: Optional filter by user surname (case-insensitive).

        Returns:
            A list of user data in DTO format.

        Raises:
            HTTPException: If an error occurs during database query.
        """
        filter_conditions = []
        if name:
            filter_conditions.append(filters.SearchFilter(field_name="name", value=name, ignore_case=True))
        if surname:
            filter_conditions.append(filters.SearchFilter(field_name="surname", value=surname, ignore_case=True))
        filter_conditions.append(filters.LimitOffset(limit=limit, offset=offset))

        results, _ = await users_service.list_and_count(*filter_conditions)
        return [UserDTO.model_validate(user) for user in results]

    @post(
        description="Create a new user with the provided data."
    )
    async def create_user(self, users_service: UserService, data: UserCreateDTO) -> UserDTO:
        """Create a new user.

        Args:
            users_service: The user service to handle database operations.
            data: The user data to create (without created/updated fields).

        Returns:
            The created user data in DTO format.

        Raises:
            HTTPException: If the data is invalid or creation fails.
        """
        user_data = data.model_dump(exclude_unset=True)
        user = await users_service.create(user_data)
        return UserDTO.model_validate(user)

    @get(
        "/{user_id:uuid}",
        description="Retrieve a specific user by their unique ID."
    )
    async def get_user(
            self,
            users_service: UserService,
            user_id: UUID = Parameter(title="User ID", description="The user to retrieve."),
    ) -> UserDTO:
        """Get a user by ID.

        Args:
            users_service: The user service to handle database operations.
            user_id: The UUID of the user to retrieve.

        Returns:
            The user data in DTO format.

        Raises:
            HTTPException: If the user is not found (404).
        """
        user = await users_service.get(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return UserDTO.model_validate(user)

    @put(
        "/{user_id:uuid}",
        description="Update an existing user by ID. You can update name, surname, and password fields partially."
    )
    async def update_user(
            self,
            users_service: UserService,
            data: UserUpdateDTO = Body(
                title="User Update Data",
                description="The updated user data (partial updates allowed).",
            ),
            user_id: UUID = Parameter(title="User ID", description="The ID of the user to update."),
    ) -> UserDTO:
        """Update a user.

        Args:
            users_service: The user service to handle database operations.
            data: The updated user data (partial updates allowed).
            user_id: The UUID of the user to update.

        Returns:
            The updated user data.

        Raises:
            HTTPException: If the user is not found (404) or no fields are provided for update (400).
        """
        user = await users_service.get(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        update_data = data.model_dump(exclude_unset=True)
        if not update_data:
            raise HTTPException(status_code=400, detail="No fields provided for update")

        user = await users_service.update(update_data, item_id=user_id, auto_commit=True)
        return UserDTO.model_validate(user)

    @delete(
        "/{user_id:uuid}",
        description="Delete a specific user by their unique ID."
    )
    async def delete_user(
            self,
            users_service: UserService,
            user_id: UUID = Parameter(title="User ID", description="The user to delete."),
    ) -> None:
        """Delete a user.

        Args:
            users_service: The user service to handle database operations.
            user_id: The UUID of the user to delete.

        Returns:
            None

        Raises:
            HTTPException: If the user is not found (404).
        """
        user = await users_service.get(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        await users_service.delete(user_id)