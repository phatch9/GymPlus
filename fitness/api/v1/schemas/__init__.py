"""
Validation schemas using Marshmallow
Handle request validation and response serialization
"""

from marshmallow import Schema, fields, validate, pre_load, post_load


# ============================================================================
# USER SCHEMAS
# ============================================================================

class UserSchema(Schema):
    """Schema for user data"""
    id = fields.Int(dump_only=True)
    first_name = fields.Str(required=True, validate=validate.Length(min=1, max=60))
    last_name = fields.Str(required=True, validate=validate.Length(min=1, max=60))
    email = fields.Email(required=True)
    password = fields.Str(required=True, load_only=True, validate=validate.Length(min=8))
    calories_consumed = fields.Int(dump_only=True)
    calories_burned = fields.Int(dump_only=True)
    user_perk = fields.Int(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


class UserUpdateSchema(Schema):
    """Schema for updating user data"""
    first_name = fields.Str(validate=validate.Length(min=1, max=60))
    last_name = fields.Str(validate=validate.Length(min=1, max=60))
    email = fields.Email()
    password = fields.Str(validate=validate.Length(min=8), load_only=True)


class UserStatsSchema(Schema):
    """Schema for user statistics"""
    user_id = fields.Int()
    total_workouts = fields.Int()
    total_calories_burned = fields.Int()
    total_calories_consumed = fields.Int()
    current_streak = fields.Int()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()


# ============================================================================
# EXERCISE SCHEMAS
# ============================================================================

class ExerciseSchema(Schema):
    """Schema for exercise data"""
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    description = fields.Str()
    category = fields.Str(required=True, validate=validate.OneOf(['strength', 'cardio', 'flexibility', 'yoga']))
    muscle_group = fields.Str()
    difficulty = fields.Str(required=True, validate=validate.OneOf(['beginner', 'intermediate', 'advanced']))
    equipment = fields.Str()
    instructions = fields.Str()
    video_url = fields.Url()
    image_url = fields.Url()
    calories_per_minute = fields.Int()
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


class ExerciseUpdateSchema(Schema):
    """Schema for updating exercise data"""
    name = fields.Str(validate=validate.Length(min=1, max=100))
    description = fields.Str()
    category = fields.Str(validate=validate.OneOf(['strength', 'cardio', 'flexibility', 'yoga']))
    muscle_group = fields.Str()
    difficulty = fields.Str(validate=validate.OneOf(['beginner', 'intermediate', 'advanced']))
    equipment = fields.Str()
    instructions = fields.Str()
    video_url = fields.Url()
    image_url = fields.Url()
    calories_per_minute = fields.Int()


# ============================================================================
# WORKOUT SCHEMAS
# ============================================================================

class WorkoutExerciseSchema(Schema):
    """Schema for exercise within a workout"""
    id = fields.Int(dump_only=True)
    exercise_id = fields.Int(required=True)
    exercise_name = fields.Str(dump_only=True)
    sets = fields.Int()
    reps = fields.Int()
    weight = fields.Float()
    duration_seconds = fields.Int()
    distance = fields.Float()
    calories = fields.Int()
    order = fields.Int(dump_only=True)


class WorkoutExerciseCreateSchema(Schema):
    """Schema for creating workout exercise"""
    exercise_id = fields.Int(required=True)
    sets = fields.Int()
    reps = fields.Int()
    weight = fields.Float()
    duration_seconds = fields.Int()
    distance = fields.Float()
    calories = fields.Int()


class WorkoutHistorySchema(Schema):
    """Schema for workout history"""
    id = fields.Int(dump_only=True)
    user_id = fields.Int(dump_only=True)
    workout_name = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    workout_type = fields.Str(required=True, validate=validate.OneOf(['cardio', 'strength', 'mixed', 'flexibility', 'yoga']))
    duration_minutes = fields.Int()
    calories_burned = fields.Int()
    notes = fields.Str()
    date_completed = fields.DateTime(dump_only=True)
    exercises = fields.Nested(WorkoutExerciseSchema, many=True, dump_only=True)


class WorkoutCreateSchema(Schema):
    """Schema for creating a workout"""
    workout_name = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    workout_type = fields.Str(required=True, validate=validate.OneOf(['cardio', 'strength', 'mixed', 'flexibility', 'yoga']))
    duration_minutes = fields.Int()
    calories_burned = fields.Int()
    notes = fields.Str()
    exercises = fields.Nested(WorkoutExerciseCreateSchema, many=True, missing=[])


class WorkoutUpdateSchema(Schema):
    """Schema for updating a workout"""
    workout_name = fields.Str(validate=validate.Length(min=1, max=100))
    workout_type = fields.Str(validate=validate.OneOf(['cardio', 'strength', 'mixed', 'flexibility', 'yoga']))
    duration_minutes = fields.Int()
    calories_burned = fields.Int()
    notes = fields.Str()


# ============================================================================
# TODO SCHEMAS
# ============================================================================

class TodoSchema(Schema):
    """Schema for todo data"""
    id = fields.Int(dump_only=True)
    user_id = fields.Int(dump_only=True)
    title = fields.Str(required=True, validate=validate.Length(min=1, max=200))
    completed = fields.Bool(missing=False)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


class TodoUpdateSchema(Schema):
    """Schema for updating todo data"""
    title = fields.Str(validate=validate.Length(min=1, max=200))
    completed = fields.Bool()


# ============================================================================
# ERROR RESPONSE SCHEMA
# ============================================================================

class ErrorSchema(Schema):
    """Schema for error responses"""
    error = fields.Str()
    message = fields.Str()
    details = fields.Dict()
