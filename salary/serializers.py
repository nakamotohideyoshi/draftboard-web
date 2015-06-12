from rest_framework import serializers
from .models import SalaryConfig, TrailingGameWeight

class TrailingGameWeightSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrailingGameWeight
        fields = ( "through", "weight")

class SalaryConfigSerializer(serializers.ModelSerializer):
    trailing_game_weights = TrailingGameWeightSerializer(many=True, read_only=False)

    def create(self, validated_data):
        tgw_data_arr = validated_data.pop('trailing_game_weights')
        salary_config = SalaryConfig.objects.create(**validated_data)
        for tgw in tgw_data_arr:
            TrailingGameWeight.objects.create(salary=salary_config, **tgw)
        return salary_config

    class Meta:
        model = SalaryConfig
        fields = ("pk","trailing_games", "days_since_last_game_flag", "min_games_flag", "min_player_salary", "max_team_salary", "min_avg_fppg_allowed_for_avg_calc", "trailing_game_weights")




