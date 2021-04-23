import graphene
import json
from datetime import datetime
from graphene_django.types import DjangoObjectType
from .models import Launch, Rocket, Payload, LaunchSite, Norad
import time


class LaunchSiteType(DjangoObjectType):

    class Meta:
        model = LaunchSite

class NoradType(DjangoObjectType):

    class Meta:
        model = Norad

class PayloadType(DjangoObjectType):
    
    class Meta:
        model = Payload


class RocketType(DjangoObjectType):

    class Meta:
        model = Rocket
    
class LaunchType(DjangoObjectType):
    
    class Meta:
        model = Launch

class Query(graphene.ObjectType):
    
    launch = graphene.Field(LaunchType, id=graphene.Int())
    launch_by_mission_name = graphene.List(LaunchType, mission_name=graphene.String())
    launches_by_launch_date_unix = graphene.List(LaunchType, launch_date_unix=graphene.Float())
    all_launches = graphene.List(LaunchType)
    rocket = graphene.Field(RocketType, id=graphene.Int())
    all_rockets = graphene.List(RocketType)
    payload = graphene.Field(PayloadType, id=graphene.Int())
    all_payloads = graphene.List(PayloadType)
    norad = graphene.Field(NoradType, id=graphene.Int())
    all_norads = graphene.List(NoradType)
    norads_by_payload_id = graphene.List(NoradType, payload_id=graphene.String())
    launchsite = graphene.Field(LaunchSiteType, id=graphene.Int())
    all_launchsites = graphene.List(LaunchSiteType)


    def resolve_launch_by_mission_name(self, info, **kwargs):
        mission_name = kwargs.get('mission_name')

        if mission_name:
            return Launch.objects.filter(mission_name=mission_name)
        return None


    def resolve_launches_by_launch_date_unix(self, info, **kwargs):
        launch_date = kwargs.get('launch_date_unix')
        print(launch_date)
        if launch_date:
            return Launch.objects.filter(launch_date_unix=launch_date)
        return None


    def resolve_norads_by_payload_id(self, info, **kwargs):
        norad_payload_id = kwargs.get('payload_id')

        if norad_payload_id:
            payload_list = Payload.objects.filter(payload_id=norad_payload_id)
            for payload in payload_list:
                if norad_payload_id == payload.payload_id:
                    return Norad.objects.filter(payload_id=payload.id)
            return None

    def resolve_all_norads(self, info, **kwargs):
        return Norad.objects.all()

   


    def resolve_all_launchsites(self, info, **kwargs):
        return LaunchSite.objects.all()

    def resolve_all_payloads(self, info, **kwargs):
        return Payload.objects.all()

    def resolve_all_rockets(self, info, **kwargs):
        return Rocket.objects.all()

    def resolve_all_launches(self, info, **kwargs):
        return Launch.objects.all()

    
    def resolve_norad(self, info, **kwargs):
        id = kwargs.get('id')

        if id:
            return Norad.objects.get(id=id)
        return None

    def resolve_launchsite(self, info, **kwargs):
        id = kwargs.get('id')

        if id:
            return LaunchSite.objects.get(id=id)
        return None

    def resolve_payload(self, info, **kwargs):
        id = kwargs.get('id')

        if id:
            return Payload.objects.get(id=id)
        return None

    def resolve_rocket(self, info, **kwargs):
        id = kwargs.get('id')

        if id:
            return Rocket.objects.get(id=id)
        return None

    def resolve_launch(self, info, **kwargs):
        id = kwargs.get('id')

        if id:
            return Launch.objects.get(id=id)
        return None


class NoradInput(graphene.InputObjectType):
    id = graphene.ID()
    norad_id = graphene.Int()
    payload_id = graphene.Int()

class PayloadInput(graphene.InputObjectType):
    id = graphene.ID()
    payload_id = graphene.String()
    rocket_id = graphene.Int()

class LaunchSiteInput(graphene.InputObjectType):
    id = graphene.ID()
    site_id = graphene.String()
    site_name = graphene.String()
    site_name_long = graphene.String()

class RocketInput(graphene.InputObjectType):
    id = graphene.ID()
    rocket_id = graphene.String()

class LaunchInput(graphene.InputObjectType):
    id = graphene.ID()
    flight_number = graphene.Int()
    mission_name = graphene.String()
    launch_date_unix = graphene.Float()
    launch_success = graphene.Boolean()
    launchsite_id = graphene.Int()
    rocket_id = graphene.Int()


class CreateNorad(graphene.Mutation):
    class Arguments:
        input = NoradInput(required=True)
    
    ok = graphene.Boolean()
    norad = graphene.Field(NoradType)
    @staticmethod
    def mutate(root, info, input=None):
        ok = True
        payload = Payload.objects.get(id=input.payload_id)
        norad_instance = Norad( 
            norad_id = input.norad_id
        )
        norad_instance.save()
        norad_instance.payload = payload
        norad_instance.save()
        return CreateNorad(norad=norad_instance, ok=ok)

class CreateLaunchSite(graphene.Mutation):
    class Arguments:
        input = LaunchSiteInput(required=True)
    
    ok = graphene.Boolean()
    launchsite = graphene.Field(LaunchSiteType)
    @staticmethod
    def mutate(root, info, input=None):
        ok = True
        launchsite_instance = LaunchSite( 
            site_id = input.site_id,
            site_name = input.site_name,
            site_name_long = input.site_name_long
        )
        launchsite_instance.save()
        return CreateLaunchSite(launchsite=launchsite_instance, ok=ok)

class CreatePayload(graphene.Mutation):
    class Arguments:
        input = PayloadInput(required=True)

    ok = graphene.Boolean()
    payload = graphene.Field(PayloadType)

    @staticmethod
    def mutate(root, info, input=None):
        ok = True
        rocket = Rocket.objects.get(id=input.rocket_id)
        payload_instance = Payload(
            payload_id = input.payload_id
        )
        payload_instance.save()
        payload_instance.rocket = rocket
        payload_instance.save()
        return CreatePayload(ok=ok,payload=payload_instance)


class CreateRocket(graphene.Mutation):
    class Arguments:
        input = RocketInput(required=True)

    ok = graphene.Boolean()
    rocket = graphene.Field(RocketType)

    @staticmethod
    def mutate(root, info, input=None):
        ok = True
        rocket_instance = Rocket(
            rocket_id = input.rocket_id
        )
        rocket_instance.save()
        return CreateRocket(ok=ok,rocket=rocket_instance)


class CreateLaunch(graphene.Mutation):
    class Arguments:
        input = LaunchInput(required=True)
    
    ok = graphene.Boolean()
    launch = graphene.Field(LaunchType)
    @staticmethod
    def mutate(root, info, input=None):
        ok = True
        
        launch_instance = Launch( 
            flight_number = input.flight_number,
            mission_name = input.mission_name,
            launch_date_unix = input.launch_date_unix,
            launch_success = input.launch_success
        )
        launch_instance.save()
        launch_site = LaunchSite.objects.get(id=input.launchsite_id)
        launch_instance.launch_site = launch_site
        rocket = Rocket.objects.get(id=input.rocket_id)
        launch_instance.rocket = rocket
        launch_instance.save()
        return CreateLaunch(launch=launch_instance, ok=ok)

class UpdateRocket(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        input = RocketInput(required=True)

    ok = graphene.Boolean()
    rocket = graphene.Field(RocketType)

    @staticmethod
    def mutate(root, info, id, input=None):
        ok = False
        rocket_instance = Rocket.objects.get(id=id)
        print(rocket_instance)
        if rocket_instance:
            ok = True
            rocket_instance.rocket_id = input.rocket_id
            rocket_instance.save()
            return UpdateRocket(ok=ok, rocket=rocket_instance)
        return UpdateRocket(ok=ok, rocket=None)


class UpdateLaunchSite(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        input = LaunchSiteInput(required=True)

    ok = graphene.Boolean()
    launchsite = graphene.Field(LaunchSiteType)

    @staticmethod
    def mutate(root, info, id, input=None):
        ok = False
        launchsite_instance = LaunchSite.objects.get(id=id)
        if launchsite_instance:
            ok = True
            launchsite_instance.site_id = input.site_id,
            launchsite_instance.site_name = input.site_name,
            launchsite_instance.site_name_long = input.site_name_long
            launchsite_instance.save()
            return UpdateLaunchSite(ok=ok, launchsite=launchsite_instance)
        return UpdateLaunchSite(ok=ok, launchsite=None)


class UpdateNorad(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        input = NoradInput(required=True)

    ok = graphene.Boolean()
    norad = graphene.Field(NoradType)

    @staticmethod
    def mutate(root, info, id, input=None):
        ok = False
        norad_instance = Norad.objects.get(id=id)
        if norad_instance:
            ok = True
            norad_instance.norad_id = input.norad_id
            norad_instance.save()
            payload = Payload.objects.get(id=input.payload_id)
            norad_instance.payload = payload
            norad_instance.save()
            return UpdateNorad(ok=ok, norad=norad_instance)
        return UpdateNorad(ok=ok, norad=None)


class UpdatePayload(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        input = PayloadInput(required=True)

    ok = graphene.Boolean()
    payload = graphene.Field(PayloadType)

    @staticmethod
    def mutate(root, info, id, input=None):
        ok = False
        payload_instance = Payload.objects.get(id=id)
        if payload_instance:
            ok = True
            payload_instance.payload_id = input.payload_id
            payload_instance.save()
            rocket = Rocket.objects.get(id=input.rocket_id)
            payload_instance.rocket = rocket
            payload_instance.save()
            return UpdatePayload(ok=ok, payload=payload_instance)
        return UpdatePayload(ok=ok, payload=None)


class UpdateLaunch(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        input = LaunchInput(required=True)

    ok = graphene.Boolean()
    launch = graphene.Field(LaunchType)

    @staticmethod
    def mutate(root, info, id, input=None):
        ok = False
        launch_instance = Launch.objects.get(id=id)

        if launch_instance:
            ok = True
            if input.flight_number:
                launch_instance.flight_number = input.flight_number,
            launch_instance.mission_name = input.mission_name,
            if input.launch_date_unix:
                launch_instance.launch_date_unix = input.launch_date_unix,
            launch_instance.launch_success = input.launch_success
            launch_instance.save()

            launch_site = LaunchSite.objects.get(id=input.launchsite_id)
            launch_instance.launch_site = launch_site
            rocket = Rocket.objects.get(id=input.rocket_id)
            launch_instance.rocket = rocket
            launch_instance.save()
            return UpdateLaunch(ok=ok, launch=launch_instance)
        return UpdateLaunch(ok=ok, launch=None)


class DeleteNorad(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
    
    ok = graphene.Boolean()
    norad = graphene.Field(NoradType)

    @staticmethod
    def mutate(root, info, id):
        norad_instance = Norad.objects.get(id=id) 
        norad_instance.delete()
        return DeleteNorad(ok=True)
        
        return None

class DeletePayload(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
    
    ok = graphene.Boolean()
    launch = graphene.Field(PayloadType)

    @staticmethod
    def mutate(root, info, id):
        launch_instance = Payload.objects.get(id=id) 
        launch_instance.delete()
        return DeletePayload(ok=True)
        
        return None

class DeleteLaunchSite(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
    
    ok = graphene.Boolean()
    launchsite = graphene.Field(LaunchSiteType)

    @staticmethod
    def mutate(root, info, id):
        launchsite_instance = LaunchSite.objects.get(id=id) 
        launchsite_instance.delete()
        return DeleteLaunchSite(ok=True)
        
        return None

class DeleteRocket(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
    
    ok = graphene.Boolean()
    launch = graphene.Field(RocketType)

    @staticmethod
    def mutate(root, info, id):
        rocket_instance = Rocket.objects.get(id=id) 
        rocket_instance.delete()
        return DeleteRocket(ok=True)
        
        return None

class DeleteLaunch(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
    
    ok = graphene.Boolean()
    launch = graphene.Field(LaunchType)

    @staticmethod
    def mutate(root, info, id):
        launch_instance = Launch.objects.get(id=id) 
        launch_instance.delete()
        return DeleteLaunch(ok=True)
        
        return None

class Mutation(graphene.ObjectType):
    create_launch = CreateLaunch.Field()
    update_launch = UpdateLaunch.Field()
    delete_launch = DeleteLaunch.Field()
    create_rocket = CreateRocket.Field()
    update_rocket = UpdateRocket.Field()
    delete_rocket = DeleteRocket.Field()
    create_launchsite = CreateLaunchSite.Field()
    update_launchsite = UpdateLaunchSite.Field()
    delete_launchsite = DeleteLaunchSite.Field()
    create_payload = CreatePayload.Field()
    update_payload = UpdatePayload.Field()
    delete_payload = DeletePayload.Field()
    create_norad = CreateNorad.Field()
    update_norad = UpdateNorad.Field()
    delete_norad = DeleteNorad.Field()
    

schema = graphene.Schema(query=Query, mutation=Mutation)