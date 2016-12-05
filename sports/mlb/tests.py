#
# sports/mlb/tests.py

from ast import literal_eval
from test.classes import AbstractTest
import sports.mlb.models
from dataden.watcher import OpLogObj, OpLogObjWrapper
from dataden.cache.caches import LiveStatsCache
from sports.mlb.parser import (
    SeasonSchedule,
    GameSchedule,
    TeamHierarchy,
    PbpParser,  # new mlb linked data parser/sender
    GameBoxscores,

    # caches
    PitchCache,
    AtBatCache,
    PitcherCache,
    RunnerCache,

    # Req[uirement] objects
    ReqPitch,
    ReqAtBat,
    ReqPitcher,
    ReqRunner,
)
from sports.trigger import MlbOpLogObj

class CustomMlbAtBatLivestatPassesAsNewObjectTest(AbstractTest):

    def setUp(self):
        super().setUp()
        self.cache_class = LiveStatsCache

    def test_1(self):

        cache = self.cache_class(clear=True)

        at_bat_no_description_obj = {
            'dd_updated__id': 1469581577314,
            'game__id': '530ca8e9-dd8a-4c19-9ba2-1f25a2ea8818',
            'hitter_id': '31d992e8-1016-484a-b7c3-2b5851442cc5',
            'id': '5baa2323-c8cb-476a-ba1e-0c0de56b370a',
            'parent_api__id': 'pbp',
            'pitchs': [{'pitch': 'c108e24b-e60e-451a-91d9-86fb576865a1'},
                       {'pitch': '783c97f1-9a36-4645-8de6-9d9de77bef6b'},
                       {'pitch': 'd113b5c5-55f4-4b73-a63d-268f1d1f44f6'},
                       {'pitch': 'c4573125-c646-4ca9-8232-05e8686301ee'},
                       {'pitch': 'd337ddf6-7b0a-495f-92db-e48fddca9c11'},
                       {'pitch': 'd17d7831-50db-47ee-8f43-0f57495b0903'}],
            'steal': 'dc649929-dbc0-4406-845b-20059552bcd1'
        }
        # wrap it with the oplog wrapper so itll work
        data = OpLogObjWrapper.wrap(at_bat_no_description_obj, ns='mlb.at_bat')
        at_bat_no_description = MlbOpLogObj(data)

        self.assertTrue(at_bat_no_description.override_new())

        # # add 1st time - should always return true 1st time
        # self.assertTrue( cache.update(olo) )
        # # add 2nd time, a normal OpLogObj would return false, but this should be True
        # # beacuse of its namespace (ie: its 'ns') and it has no 'description' field yet
        # self.assertTrue( cache.update(at_bat_olo_no_description) )
        #
        # # once it has a description field it will pass the filter only once more
        # at_bat_with_description = {
        #   'dd_updated__id': 1469581577314,
        #   'description': 'Joe Mauer strikes out swinging.',
        #   'game__id': '530ca8e9-dd8a-4c19-9ba2-1f25a2ea8818',
        #   'hitter_id': '31d992e8-1016-484a-b7c3-2b5851442cc5',
        #   'id': '5baa2323-c8cb-476a-ba1e-0c0de56b370a',
        #   'parent_api__id': 'pbp',
        #   'pitchs': [{'pitch': 'c108e24b-e60e-451a-91d9-86fb576865a1'},
        #    {'pitch': '783c97f1-9a36-4645-8de6-9d9de77bef6b'},
        #    {'pitch': 'd113b5c5-55f4-4b73-a63d-268f1d1f44f6'},
        #    {'pitch': 'c4573125-c646-4ca9-8232-05e8686301ee'},
        #    {'pitch': 'd337ddf6-7b0a-495f-92db-e48fddca9c11'},
        #    {'pitch': 'd17d7831-50db-47ee-8f43-0f57495b0903'}],
        #   'steal': 'dc649929-dbc0-4406-845b-20059552bcd1'
        # }
        #
        # at_bat_with_description = MlbOpLogObjWrapper('mlb', 'at_bat', data)
        # # 1st time True -- because its changed
        # self.assertTrue(cache.update(at_bat_with_description))
        # # false the second time (its no longer changed, nor bypassing
        # self.assertFalse(cache.update(at_bat_with_description))

class GameBoxscoresParserManagerClassTest(AbstractTest):

    def setUp(self):
        super().setUp()
        self.parser = GameBoxscores()

    def __parse_and_send(self, unwrapped_obj, target):
        # oplog_obj = OpLogObjWrapper('nflo', 'play', unwrapped_obj)
        # self.parser.parse(oplog_obj, target=('nflo.play', 'pbp'))
        parts = target[0].split('.')
        oplog_obj = OpLogObjWrapper(parts[0], parts[1], unwrapped_obj)
        self.parser.parse(oplog_obj, target=target)
        print('self.o:', str(self.parser.o))
        print('about to call send()...')
        self.parser.send()
        print('... called send()')

    def test_1(self):
        sport_db = 'mlb'
        parent_api = 'boxscores'
        data = {
            "_id": "cGFyZW50X2FwaV9faWRib3hzY29yZXNpZGM4MjQ1NmFjLWE0YjktNGNhZi04MTI0LTBhZmE3NGY5Y2YzNA==",
            "attendance": 37441,
            "away_team": "27a59d3b-ff7c-48ea-b016-4798f560f5e1",
            "coverage": "full",
            "day_night": "N",
            "game_number": 1,
            "home_team": "43a39081-52b4-4f93-ad29-da7f329ea960",
            "id": "c82456ac-a4b9-4caf-8124-0afa74f9cf34",
            "scheduled": "2015-05-10T01:10:00+00:00",
            "status": "closed",
            "xmlns": "http://feed.elasticstats.com/schema/baseball/v5/game.xsd",
            "parent_api__id": "boxscores",
            "dd_updated__id": 1431234264301,
            "venue": "f1c03dac-3c0f-437c-a325-8d5702cd321a",
            "broadcast__list": {
                "network": "ROOT SPORTS"
            },
            "final__list": {  ##### when the game is OVER it holds this
                "inning": 9,
                "inning_half": "T"
            },
            "home": "43a39081-52b4-4f93-ad29-da7f329ea960",
            "away": "27a59d3b-ff7c-48ea-b016-4798f560f5e1",
            "pitching__list": {
                "win__list": {
                    "player": "9760f1d6-9560-45ed-bc73-5ec2205905a2"
                },
                "loss__list": {
                    "player": "a193c72e-e252-49c4-8ae5-2836039afda7"
                },
                "hold__list": {
                    "player": "6f61629a-8c64-4469-b67a-48d470b7c990"
                }
            }
        }

        self.__parse_and_send(data, (sport_db + '.' + 'game', parent_api))

class TestSeasonScheduleParser(AbstractTest):
    """
    tests sports.mlb.parser.SeasonSchedule
    """

    def setUp(self):
        super().setUp()
        self.obj_str = """{'league__id': '2fa448bc-fc17-4d3d-be03-e60e080fdc26', 'year': 2015.0, 'games__list': [{'game': '00652d0b-b72b-408d-a8a0-5e185079e180'}, {'game': '01881168-1bc9-4abc-9e14-ab6aac534222'}, {'game': '022acf07-809b-4585-b278-061067a3f423'}, {'game': '027f9c22-c85f-45fd-9ac2-e0668aea5541'}, {'game': '03887460-5886-4cd2-b120-db2666445a19'}, {'game': '040c72b1-f3fd-4e0a-901a-3046e81a182c'}, {'game': '0440e6db-8886-4597-855c-c747b404e0fc'}, {'game': '044447e0-f1b5-4b70-bdcf-a62867320054'}, {'game': '044f6dd7-ad0a-4924-a7c5-44ce6b3e20b4'}, {'game': '04627626-4b46-404a-b1c4-35029450f3ca'}, {'game': '048cb514-df39-44de-8ffd-62a2e4484d45'}, {'game': '04fd2031-8053-4a29-8be2-22e45acfbb7e'}, {'game': '056dd5c1-d479-4b1c-b25f-73580568af11'}, {'game': '065e7997-7d7b-413d-b3c7-90eeec0a9c94'}, {'game': '06f8be3e-dfa4-49f2-9b36-b97bb086d224'}, {'game': '0746ce83-8368-4b00-9289-cde29ae7659a'}, {'game': '0888817e-2017-4815-b92e-bcfa5ce7dbcb'}, {'game': '08e10021-2f40-43eb-8eba-21039e675b13'}, {'game': '09b20afc-11ae-4a34-804b-39aa0956c70c'}, {'game': '09c8344e-cc66-496c-bef1-2d406852c4b7'}, {'game': '09e93365-e3e5-4de5-85d1-2d4433575820'}, {'game': '0b1642f3-32af-42b6-a4df-a8f5113863ba'}, {'game': '0bbc43a5-4da8-4c67-85d0-33d36793e6d9'}, {'game': '0bc814b7-898f-4ccb-8544-339db3fc6a4e'}, {'game': '0c69ccc3-acd1-47aa-afe4-9317ee7325f1'}, {'game': '0ccb3bc9-a7f3-4f22-bfde-c138f697dd6e'}, {'game': '0d229647-31cf-4a4c-ac38-9ff9a924e9f5'}, {'game': '0d2d976d-0529-4ad1-9e0b-a42d645f1418'}, {'game': '0d99414c-2560-42ce-b3fe-746816bc8439'}, {'game': '0ea529a3-5e36-4eee-b192-551a50b45eb4'}, {'game': '0f6d795d-3bc2-404b-bb18-20d547584008'}, {'game': '101d0243-7d34-406e-bee8-ab5ca27ea610'}, {'game': '106c3f49-c595-4cbf-978c-7e703a4de60f'}, {'game': '11e7cc89-4380-48e1-8ad4-3dc51fa41584'}, {'game': '121e8ac9-7cea-439b-9d0f-30d8660878f9'}, {'game': '1227772a-6f9f-4d54-8699-1bf25a93b0c3'}, {'game': '14215728-6bbf-43bb-a7f3-639234d91344'}, {'game': '1489fe4b-dca9-4bca-97bd-0c3185e3c566'}, {'game': '149e5157-8960-44c1-9667-a724acebb0fd'}, {'game': '14dad102-7f23-47e2-a184-fe29f3afb838'}, {'game': '14f3f27f-dde7-4a8e-b843-67de4a862dd0'}, {'game': '14f65ff3-5ba6-47c2-b64f-4a034eee1262'}, {'game': '161265f7-b7cf-486b-ba73-22b58d541a51'}, {'game': '162d114f-f755-4271-b41e-f232cc6ee4e3'}, {'game': '16c30329-f445-4cf8-8ee0-ffc8bd8907b0'}, {'game': '173664ca-3d47-4f0b-9cdb-b68a761d7402'}, {'game': '176814b8-8988-445c-ba84-3a953f6bc02c'}, {'game': '17b6f704-b588-4d37-9761-a67a34e7e59f'}, {'game': '17b8890a-9390-4980-91c2-6a8264d3d6ce'}, {'game': '192c94e9-8f2b-4f10-906c-7197642ad61e'}, {'game': '1a889f0b-7f64-4d3f-ba76-236ebf811a54'}, {'game': '1bf2c922-dc54-4321-8ed4-e5d1a52f8b2a'}, {'game': '1c4cb6a8-532b-49a2-9b7d-bc45165da6c9'}, {'game': '1c98d98b-d4cf-4923-a4f8-5a08e5a61ef8'}, {'game': '1ceefca0-004e-4790-85d7-a17ec1602e4d'}, {'game': '1d451722-d7a7-4bf2-a144-054326733a3c'}, {'game': '1db0f424-5091-4ecc-8639-246b87ecdaf5'}, {'game': '1e1e31f8-db7a-4e4b-8e1c-6178089f0704'}, {'game': '1e553f50-a104-4cd8-b8ed-778a60221feb'}, {'game': '1f72caf7-9d13-4e5c-b584-50643451d66b'}, {'game': '1f8c3298-1354-4c05-974f-8ba7af244cbd'}, {'game': '1f9e9e93-f17e-4851-8de2-a940a270e032'}, {'game': '1fed7c34-f1f1-4061-9f2d-59f2f55987f9'}, {'game': '2032f6cd-a9d0-4d22-8697-b9531ba9e68c'}, {'game': '2056559e-dee9-4f3b-afc4-e19932bd7235'}, {'game': '206b485c-fd93-47ed-a77b-ddc107d84fac'}, {'game': '2094f264-9a64-4e61-9a8c-cdb046aeaf65'}, {'game': '20c1307d-cff2-4fc6-a8e6-6164d7775da0'}, {'game': '21303d6d-2a80-4fac-886d-62ef04d30b78'}, {'game': '21672692-adb4-4aa5-bc11-d8793a663382'}, {'game': '217271ba-4d46-4650-a863-83c3a48caa53'}, {'game': '22023e10-65f2-4c15-8ec3-4a360992038d'}, {'game': '22482438-2a81-4e74-9e3c-17ae61256a42'}, {'game': '2256478f-7809-417c-8fb8-c63a00943afa'}, {'game': '2268fa72-2676-4eef-a0d7-662a9cf68fa0'}, {'game': '228b349a-7909-4e3d-bee8-55dc1d4b0815'}, {'game': '22b9f081-3edf-450f-a7d5-b00394e2b1a7'}, {'game': '22cd311e-75e0-4cc9-9aff-611fc3f6a0f0'}, {'game': '22d32449-e8f9-4f58-acb9-96ec5da8d3dc'}, {'game': '2319839e-f37d-4044-bbeb-6d06790fdbaa'}, {'game': '236cdb72-d3b5-4ec1-9380-476cd4e9c8c4'}, {'game': '2472ea1a-faa0-4780-a2d4-684ff689ec1b'}, {'game': '24abd3a6-f655-49e0-845f-51f37b5b2a61'}, {'game': '24cb0c24-ebd8-4010-9be2-a49caac0dc87'}, {'game': '2557cf18-b5f4-4303-ba0e-69b5164ed0f4'}, {'game': '256a78a3-3cda-4321-8362-346848675063'}, {'game': '2585f9ff-d7bb-4882-9d7f-263659fdac6d'}, {'game': '258af261-6c3a-4c4e-9689-df614e832801'}, {'game': '26178e13-8f1a-4704-9840-56b63cc54a5f'}, {'game': '262143f2-69dc-487b-a878-aad23e72c898'}, {'game': '27befa24-4d71-46e6-9f8c-474253c52492'}, {'game': '27c3a4eb-25c4-4568-af08-d8f3d7ff2e77'}, {'game': '28402729-cc37-4af4-a614-d619fe0300f4'}, {'game': '28476ea9-6251-434b-a5fa-30b5215cc579'}, {'game': '286758b5-fd17-4eb7-8834-825e3d9e2e80'}, {'game': '28d6ddf9-cf78-4318-b223-37859893f268'}, {'game': '29f1ea36-f5d8-4c40-b9b0-90d90572b027'}, {'game': '2a9d91a7-ef55-46bb-89aa-5a4e40e5c9ca'}, {'game': '2b05824a-e12a-4462-b6f2-54d189033a22'}, {'game': '2c24babb-8d4f-4b53-81c6-5ab432333579'}, {'game': '2c38a49e-84aa-48f6-b884-5db9b1271fee'}, {'game': '2cc0c3dc-39a3-4b09-92f8-a97057e98742'}, {'game': '2d0cd535-0430-4148-9c87-2c4487afeb58'}, {'game': '2d174b8d-8643-48fb-b987-81a069935165'}, {'game': '2d189446-b733-40a3-a3ff-2f98aa9a21f5'}, {'game': '2d27341e-a403-47d1-bbdc-66b541546728'}, {'game': '2d47d00b-40cd-467a-a2b1-be8b75b4d99d'}, {'game': '2d7c3838-71ed-42e7-a717-5039a4ada43e'}, {'game': '2dd77992-f88a-4707-8694-1421c4c9e16b'}, {'game': '2f2d8a69-0701-4eb4-b7cc-b15e93051c36'}, {'game': '2f7d7b6e-7cd8-4dc9-9060-a22f85dba7f4'}, {'game': '2fa1f125-6275-4fd4-a4c0-c1c3146877a8'}, {'game': '2ffa8b90-f545-4f65-a854-14a8acba33fc'}, {'game': '310e5e40-0f90-431b-94cf-2591bf7d695c'}, {'game': '31cf082f-58e7-4f7d-9e1a-bcb8a1720630'}, {'game': '3292ea92-7351-48c3-9477-5742fe71a2f6'}, {'game': '32c978d0-318a-4951-ae6a-1c585f4b455f'}, {'game': '3359b9ab-b06f-4c3e-8f41-a89c3d571cf7'}, {'game': '336adf39-57d0-41c5-bcb2-9cc8396a7a5b'}, {'game': '3394e9ff-a2a0-4356-860a-028172b5b8e0'}, {'game': '33c50822-bd32-40d2-8e46-92072b9a4680'}, {'game': '33db5b31-dde2-4083-b8c0-b57c739b7a12'}, {'game': '3481422f-2098-4b95-a569-44468c34bcee'}, {'game': '35867f2e-4a23-4b6c-99c2-386f6d4fbbb0'}, {'game': '372c61ef-a6b4-446a-8130-f85ff05ed30a'}, {'game': '374952e1-56ad-4e9b-a367-c5aff29184ed'}, {'game': '380a9e9d-2bd6-4a57-bfa5-c68ffb8075b5'}, {'game': '380d92e5-662d-4ba2-adeb-7870891c589d'}, {'game': '388f05e9-4520-4b11-9cfe-504e757e772c'}, {'game': '38baca79-dc43-4867-982b-4ea4082da28e'}, {'game': '397b636a-458f-4432-b41f-2409e6573ff3'}, {'game': '39dcc3a5-2fd7-4ec3-86ea-3b0377b5569b'}, {'game': '39fba605-360d-4fa9-b58f-ea81b5a64e24'}, {'game': '3b072dce-d9f9-4382-acbd-2e847ed78697'}, {'game': '3be82c7b-e23e-4526-92c5-810aa4168189'}, {'game': '3c8a9dda-6fcd-458a-89e1-aba540893875'}, {'game': '3e6d77fc-e160-48d3-b821-ea360b48600f'}, {'game': '3e6ed009-52ed-4d5a-a5ac-da74791cf7c7'}, {'game': '4049147e-2539-4b09-bd6e-d847cbe236f6'}, {'game': '412419fa-685c-4153-9243-52d3f2b3efe9'}, {'game': '41ba8e14-2b53-4a82-84c1-b66d6626e19f'}, {'game': '428c98ee-4992-4ac1-a461-690ee579752e'}, {'game': '42e47e5f-4517-4d61-a242-e60b03fa4b90'}, {'game': '4344a536-a778-4696-9bfc-5bdfb141225a'}, {'game': '43d99c9f-e1b4-4445-a5cb-27cba380b506'}, {'game': '43dba702-a720-4b97-9b97-904c8355306d'}, {'game': '43f6ce25-2638-467c-9017-62d58114bd02'}, {'game': '4528f988-bae9-4a1f-8042-247984587954'}, {'game': '456e482f-1425-40d4-8d50-595a45e63432'}, {'game': '4645cdab-ca6c-4334-8e5c-5a12bd74a10b'}, {'game': '46a8c1aa-8bc4-4810-9f61-08226166012b'}, {'game': '471aa744-6db4-4bc0-b804-1388cdc68342'}, {'game': '475a7b0f-2c7a-407a-a23b-fe339a38b2fd'}, {'game': '476fdc78-5a0d-498d-9e0c-260b8d3bc831'}, {'game': '4780d4c9-1b09-4855-a6b9-cba35e2c938c'}, {'game': '47fa788f-9d23-431a-a72c-a84aa0afa42d'}, {'game': '48b1e6ff-059d-44ac-bd21-d3aada2dd08a'}, {'game': '48d70492-54f6-4901-82ad-d6c30b266b2d'}, {'game': '495f5131-32f9-4baa-b751-861b13a85d60'}, {'game': '49affd4b-db66-48ad-999c-d0672abe228f'}, {'game': '4a7ed594-c643-4025-988c-da7efb6b5c7e'}, {'game': '4c2296c1-5378-45ed-947a-cfbcc159b7c9'}, {'game': '4c903229-6603-448f-b55f-d9858b9f44ed'}, {'game': '4cf3a530-4129-4795-858f-4f7e58690e39'}, {'game': '4d1b55e1-307b-4240-934a-764ca1060aed'}, {'game': '4d7c4aeb-4567-438e-aba0-9ec76e483dad'}, {'game': '4e7c4b24-5785-4470-93a8-82700208e09a'}, {'game': '4e7d6c58-99dd-4b5d-8508-9604c34760b4'}, {'game': '4fa00ba9-93bf-43d6-a10b-ec5f87929ada'}, {'game': '4fb25645-6039-4fa5-97ab-10cf29c4dd45'}, {'game': '5002da0a-4189-49fb-8e28-480dd8e439ae'}, {'game': '50464669-79a6-4e87-8490-1b5f7f70e136'}, {'game': '50d6e32e-8512-4527-9af5-722850a87312'}, {'game': '5248350c-6aca-42b3-8861-ea658cd9a73e'}, {'game': '5279bf70-21c3-40b1-b4a0-0a2bd7160a68'}, {'game': '52ed8f28-1bf3-4aa5-b1b4-477f637b57cd'}, {'game': '562ffd51-d490-429f-8ba2-cfe4f2c28b9a'}, {'game': '563dcc75-0817-4b73-9d61-804cb2dba6b5'}, {'game': '56fce3ec-460b-480c-a99f-1cd5a7dc6981'}, {'game': '57bb8e88-3bbb-4841-9d2f-e2593aebc607'}, {'game': '57da8f89-281f-4840-ac39-6417041aac7a'}, {'game': '5837c0cc-a391-469c-b8a4-5a37f942c489'}, {'game': '588c4751-63b1-4c30-85f3-4a1d25f2182e'}, {'game': '58ff06c5-0d0c-48a7-8124-03a98a04a822'}, {'game': '5a4413a7-925d-4a6a-b8c8-5889e62bdc2a'}, {'game': '5b5fb769-abcc-4327-a537-0df3f5c3777c'}, {'game': '5b98fc2c-c8c5-4c45-84d4-7a96072daaa8'}, {'game': '5c1644a8-7685-48f6-97b6-5a1447edc770'}, {'game': '5c80ba93-5813-4c7f-ad1b-6421f93ef551'}, {'game': '5d49ef6c-a631-4fa8-bbbb-bbc50ca18760'}, {'game': '5e22bdc2-a9d9-436a-9079-68124fd09e71'}, {'game': '5ea5fd84-19d6-47c3-bb41-8d492d61ce41'}, {'game': '5ed35d28-ae0d-4758-8012-736de10b7677'}, {'game': '5f02de16-c240-485b-9d16-bfb19e9bc6d3'}, {'game': '60d4b97b-3704-47c6-84aa-15a04a043d08'}, {'game': '60d80ce2-b6fd-4c23-90de-7e965838e879'}, {'game': '6184be47-2c15-4e22-aeb6-f86e7c24e75f'}, {'game': '61becf20-2b96-48af-bd58-bbba73b2acba'}, {'game': '621da31e-89d6-4b43-afdd-688ce7bb2bc9'}, {'game': '62720dae-7d81-4ce2-a220-51beb9012cf7'}, {'game': '63572cfd-4ded-427e-a41d-e087bf048a3f'}, {'game': '639bfc21-f179-449a-8702-911b5f13514f'}, {'game': '63a8745a-709f-44b4-84ca-9a6a2eff02ac'}, {'game': '6497d28b-225d-494b-9dbd-1036704c24cf'}, {'game': '65cc7396-2b8a-41dd-bd83-3f7a45ab10be'}, {'game': '664c4e4d-9035-4a6a-9fd5-8e2998dbc070'}, {'game': '66693e5e-7cba-40a5-bcb5-2e65cea08a18'}, {'game': '66caaa12-daac-4cb8-91e7-12624003a883'}, {'game': '68dda550-fb87-4d5f-b5a5-eccebe84c0b1'}, {'game': '6916385f-1243-4320-a9f3-be69bd58169e'}, {'game': '694750ff-51da-4afc-8346-c832ffe1c6ff'}, {'game': '6aee8b7b-9f53-4dfb-bfc6-6297009ef97d'}, {'game': '6b193c17-e351-4fae-b04e-d6bb70b4ff7f'}, {'game': '6b67c137-2dc6-4df4-8995-dbe65137cf4a'}, {'game': '6bc5ade6-aea5-4c5b-b71d-a0fa1befcebe'}, {'game': '6bcd7f46-6b60-424c-90db-d0ce8971cb7c'}, {'game': '6c1dee74-e615-4a5c-bf37-6874b3e5e12a'}, {'game': '6cc87cf1-4f21-4fc5-a2d6-8125732506fa'}, {'game': '6d2774d2-4ded-487c-a070-a178d02c62f1'}, {'game': '6e452dbf-66b8-4a72-a972-1dcc0d7523f6'}, {'game': '6f60d762-32d4-4e22-b17e-9462541e2cad'}, {'game': '718468e0-360e-4896-a0f4-b28291addb74'}, {'game': '7202dba6-f0e7-44f7-83ab-32ad16453bba'}, {'game': '723d3f29-1d54-4df2-93de-92910d38bde3'}, {'game': '7252a3fb-232f-4cce-81c8-5c271be0df7c'}, {'game': '72d94caa-fb64-4e76-927f-9443278c0b9d'}, {'game': '73953683-17cf-4310-8195-a77d2afa4828'}, {'game': '73b42968-358c-4029-a551-913cf848f1b9'}, {'game': '73cf5f54-4c76-4f57-9039-aae64563f58e'}, {'game': '744ad4d7-5c26-4acf-94a6-135cbbb7e821'}, {'game': '7570a3ac-98fd-4d36-a4cd-a8b47647df26'}, {'game': '7582460c-e769-4be7-9f8a-da6d8a3688f2'}, {'game': '760b9b17-2942-44c6-8793-35736f367d1e'}, {'game': '764c31aa-d328-4a7c-af2b-f82e76263ba7'}, {'game': '779ddf6a-6534-4583-a781-b56256895f5e'}, {'game': '7803fc44-703f-4a4d-9c0b-29dd5dfefa62'}, {'game': '7857de42-a8b1-4a09-8819-af61645461eb'}, {'game': '78a09c50-0382-47ab-8de7-0559e87c64b7'}, {'game': '78ada840-928c-4d72-bf17-ac850525c229'}, {'game': '7953d79f-d678-4ee6-ab07-a80b2845c944'}, {'game': '79b9e0ec-f260-4114-b226-d228586204f6'}, {'game': '79c1e96a-b457-4192-8cc5-a4750e11eccc'}, {'game': '79c67c74-c6fb-4ae3-88c5-caf4126bd8b5'}, {'game': '79cf7774-b63c-4b3b-b837-3986ec85b09f'}, {'game': '79de39c0-64f6-45b5-9c26-14f636d669f1'}, {'game': '7a7a0425-e8f7-4571-a1df-1fda5ad43388'}, {'game': '7a9512c9-470c-411e-bb5f-e673792a38cd'}, {'game': '7aca1977-3744-433b-8160-4b42abd8ca4d'}, {'game': '7ad903ce-bcd2-4d7c-b7c2-7c3a3aafdee5'}, {'game': '7c8a43f5-ba0a-40f0-b7f3-4371789ca091'}, {'game': '7cf47ed8-b712-41a7-8a37-3f2d086877ac'}, {'game': '7d6073e5-f4cc-430f-8027-254b18cb5460'}, {'game': '7e0bb8b4-49c7-4894-8153-94cf0a333a32'}, {'game': '7e2d4c7d-26ad-4a5f-8e2b-0b1fc325cd1c'}, {'game': '80812053-3ca6-4010-9481-37f622f71f69'}, {'game': '815bb60d-9577-4205-95cc-2329c9800a51'}, {'game': '8242e979-b14c-4303-afcf-c78383fe513a'}, {'game': '8337e6e7-96b5-4c3e-9303-fcec8d5f5900'}, {'game': '83c65af2-e6d7-49eb-a30c-aec8c75f6c1f'}, {'game': '83f114b9-8e50-401e-a62f-0755a77db16b'}, {'game': '843101ad-5f7d-49a4-a521-be1ad6c3bdc5'}, {'game': '848a2332-8b4d-4b24-8c3d-20ab2258859e'}, {'game': '852321cf-6a3e-44d3-a69c-449838484920'}, {'game': '85a6c817-0b9b-44ff-8da7-81701a3532f3'}, {'game': '85f03cbc-460c-40ca-aeac-a6e38af516c3'}, {'game': '867ed769-4efe-4489-929e-8b9dcbaae07b'}, {'game': '8695a19f-9697-45ce-84e4-2a889443711e'}, {'game': '88071057-96cc-4e32-8be5-ce5ed035df9e'}, {'game': '880cb282-5f2e-4cd5-a730-e81658053723'}, {'game': '885f354d-4756-42a2-9710-e5644c536457'}, {'game': '8868af02-09bc-4f6c-a1dc-e515103ed003'}, {'game': '887cbbd8-6c6f-4dd2-a15a-3b55ae830002'}, {'game': '88d019cd-7da9-475f-a1f8-36d74d830834'}, {'game': '898d8670-f5d3-4016-abe0-4f8e9adc9bde'}, {'game': '89a82f85-104d-4e33-958f-bc432890622f'}, {'game': '8a1d7b43-70bb-4971-b310-5d199a1e3bc5'}, {'game': '8a7a0271-509b-419e-b4c5-ebfae3ee9563'}, {'game': '8a7e0a5c-510d-48a7-82c1-4f20b7c4bbcf'}, {'game': '8dd4b177-869a-4bd7-8578-bd9848433855'}, {'game': '8f37b956-50a3-44b4-b50c-1d6c9bd6c77b'}, {'game': '8f5235f0-8122-4e6f-88cd-f083b86e3a32'}, {'game': '8f53b25c-9e72-4e72-b850-c8a748c6c232'}, {'game': '8f5c39d8-ed06-4723-a4b2-f50be368917f'}, {'game': '8f656d8e-bc6a-4ea6-9af9-f6966795266c'}, {'game': '900814b6-47c1-4dcc-a6c8-9cd1d9bd08c5'}, {'game': '903c91f3-a6dd-4065-8ead-0a2bcfec37a4'}, {'game': '91eda286-ae87-46c4-960b-550dc674e37f'}, {'game': '92301b72-722b-45a2-9d47-842b26a87267'}, {'game': '93516a5e-c0a5-4df4-89e1-2289aa9fa65d'}, {'game': '93533b20-d229-4c4e-9b3a-9a46d0f84522'}, {'game': '9390b138-0c16-43b3-b543-c1a4b8bf7770'}, {'game': '943b442c-9b27-4b20-83e0-7e04434f019d'}, {'game': '949b9356-2380-467a-b11d-032ab173212a'}, {'game': '958e4fa0-1a82-4c45-9160-4c19890254e3'}, {'game': '95ca4228-537f-4189-9f2f-4b3545eccb41'}, {'game': '96409c17-afb7-4cdf-88af-e4a2336e5a25'}, {'game': '969c7e03-d74e-490d-b9ed-2f5ac950faf1'}, {'game': '96e365f6-991a-4e8b-a6dc-7aa0ec6df0f2'}, {'game': '97f385d1-4b15-44fd-9d30-23ec66ee976b'}, {'game': '992ee2a9-ed8f-4cf8-a37a-1f3edd0f8faf'}, {'game': '9940c8f9-4132-4834-aaf8-d20cac4a21f8'}, {'game': '9a8b4472-d039-425a-8958-b3be00b004cf'}, {'game': '9a94d74f-7580-42a0-9cdb-b45d555ec212'}, {'game': '9c3f909d-d43d-4aa9-8d1a-76bbb195e869'}, {'game': '9d90e793-2da7-4d1a-8be7-983625f60c65'}, {'game': '9e3ad916-a6cc-4400-aa1c-f3c4c7f5fa97'}, {'game': '9e49184c-498b-4e04-bd89-86de3f553b51'}, {'game': '9e7172b3-b24f-4686-86e9-70eec8455eb3'}, {'game': '9ed6892c-0653-4fcf-8533-8ff814fc9920'}, {'game': '9f31b4aa-a3cb-4ace-aee6-4aa54717b4f3'}, {'game': '9f3c6c22-9dcc-4958-86ed-d53e14c9fad8'}, {'game': '9f941a4f-636a-48fe-a400-7b0dd7c41564'}, {'game': 'a0806282-7371-4d79-a311-13aa642ca44d'}, {'game': 'a0f6d1a5-7972-41e1-8846-ba8a201c59c7'}, {'game': 'a1c4e7bb-629b-45c3-afb2-5b07d63b2656'}, {'game': 'a1dacf38-ab15-4aa1-9aeb-b8fc38c29218'}, {'game': 'a1ff5d75-92cf-45a1-abdd-d70bd2a82181'}, {'game': 'a24a0c7d-901a-4e45-a835-7ad55477659f'}, {'game': 'a26fd4c2-8970-4185-83ea-136b54ea142f'}, {'game': 'a2e235c4-58f6-4300-857c-75bb617422af'}, {'game': 'a3c31c5c-d739-4a16-a3e7-d1eb34c06d75'}, {'game': 'a43600ce-5746-4fff-86c1-19220ad52e5b'}, {'game': 'a440d3b7-88af-46ec-9f25-712af5dbbf09'}, {'game': 'a441f554-b11c-4d9a-b42a-1a1908adc6b4'}, {'game': 'a4672c34-a74d-428f-aa8f-108ec88a0454'}, {'game': 'a52e76c6-78e4-48dc-a58f-20fd9fc9ba47'}, {'game': 'a60e2bbb-1cb4-4232-ab8d-a0001a32cf6d'}, {'game': 'a66f9ef8-96b9-4e8b-9df5-1417db155d22'}, {'game': 'a76be862-1788-49db-b6c6-c3834187b0fd'}, {'game': 'a7a922a9-92f7-40f6-987b-1fad721306b7'}, {'game': 'a7aad591-949c-4ca0-a966-9f5cd687e5be'}, {'game': 'a7e366f9-a741-4a07-9cd3-14821c5870c6'}, {'game': 'a87342ec-86c1-45d8-813b-f8dcabb97a51'}, {'game': 'a8e8c1e6-15a7-47d7-8d25-19544c7f8997'}, {'game': 'a92f8d7f-27f1-4414-92d2-9bbc67227f3f'}, {'game': 'a99ed546-05e7-4589-bb73-cb49a7d781d3'}, {'game': 'aa8093e5-535b-4893-b900-eed2ca7d56ff'}, {'game': 'aba197d5-ad51-4398-959f-02e785dd045f'}, {'game': 'abbc2faa-f206-4508-91ab-4dfce4e5f429'}, {'game': 'ac233372-0dda-4de9-b778-c5c63acf6b90'}, {'game': 'ad4b9140-02df-43a5-9752-a79e65ea0023'}, {'game': 'ad55db1b-c8a6-42be-b308-c80d115082d8'}, {'game': 'ad83f17c-f528-47e2-ba75-874630a397b0'}, {'game': 'addd7055-f42e-4f83-bc63-3123de9ef63f'}, {'game': 'adde768e-ddf4-4950-9937-72e7101369ac'}, {'game': 'ae24d317-df1a-4caf-8a4a-08118cbe065b'}, {'game': 'ae29a2af-fe02-48d1-9a11-f7a659f8cf0f'}, {'game': 'af9f74f3-6d2f-442a-873d-d79595339cc1'}, {'game': 'aff36777-21db-4d68-8100-d87af3c8e5e7'}, {'game': 'b0c21776-4e2c-4680-a511-959b658d0500'}, {'game': 'b0c8d08a-e28a-4902-814e-44c3fcd54fdb'}, {'game': 'b0dafd3d-47c4-4c0a-aa8d-64422884323f'}, {'game': 'b26081f7-3350-4d1e-8921-7fc9aa0a1359'}, {'game': 'b27c79fb-a514-458f-9ae1-e798f0e126cc'}, {'game': 'b28fa8c4-bd51-4379-831f-6facc328b56b'}, {'game': 'b2c2d6d3-c4ee-4bdc-ba38-f7fe89ccf44e'}, {'game': 'b39734b3-61ce-4e49-97b2-cb19d8a12280'}, {'game': 'b3d7e0d8-9dca-479e-b708-fee83ebdc27b'}, {'game': 'b3e8fb36-c34a-4fad-a7f6-5c727e5c208d'}, {'game': 'b4820075-1b26-45c3-98de-f4f3f9c2f7b6'}, {'game': 'b498bdd0-81e3-466e-be3a-fc833417ae5c'}, {'game': 'b4993945-857e-4767-bc5f-cdc686ebc38b'}, {'game': 'b535edcf-6838-4e46-b5f6-f78f2078b198'}, {'game': 'b5d41f40-b362-4243-af25-7520b3af516f'}, {'game': 'b5dd2cf2-f805-4af9-81eb-2a6d6dd07317'}, {'game': 'b5e0a916-a84e-48c9-b77c-64d41d1b3102'}, {'game': 'b771a9f6-11ba-4f2a-903a-5a4195cedd6e'}, {'game': 'ba8efd37-6338-4007-84ab-e71b832a8593'}, {'game': 'bae8e625-7493-4d3c-b10d-a28ce53c5e7b'}, {'game': 'bb056f6e-1f3e-487b-94a3-a44c268c8da2'}, {'game': 'bba327ef-4725-4847-92bd-da12464c8f78'}, {'game': 'bc5ac2be-77ff-4ed0-a6e6-b91fb5a329f2'}, {'game': 'bde1ae57-ecec-4782-8d93-c8f16ad8e67a'}, {'game': 'be833d2b-b416-4149-882a-8250710b9c07'}, {'game': 'bf2458ae-ac3e-41ed-a4aa-e1a0af4cc732'}, {'game': 'bf271e3b-2201-41d7-ac2e-1d4b8e8a9903'}, {'game': 'c0bbf3aa-ab27-4918-971c-25f5b5e6b372'}, {'game': 'c1677c0a-5fe2-4aa6-a208-81d182fc80a2'}, {'game': 'c201e9ab-df4f-406e-b11d-604154072c8e'}, {'game': 'c20cb4b0-c100-4834-8ece-15c4c11c3f33'}, {'game': 'c32e1bb9-115a-4ca9-a706-8f71626e48f4'}, {'game': 'c5ba5df8-a958-4ef3-ad9e-e87fbb92bbab'}, {'game': 'c5de4730-baf8-4ef6-97c4-73adf81ed3a3'}, {'game': 'c5ed702d-f86f-45fe-9bc0-4e09908b6514'}, {'game': 'c6595e45-2c4a-47d4-8f00-5d5ef91bafba'}, {'game': 'c68cfd35-52d0-415f-92a0-1f945792ae51'}, {'game': 'c7c6884f-7f99-427b-afda-3455dc2e8962'}, {'game': 'c7f475b6-eb4b-4f19-9500-22b4c07fa2ad'}, {'game': 'c87dd075-8690-460b-a93d-47e477535251'}, {'game': 'c8ab2f5d-8683-4ff0-aed1-2436095ca2bd'}, {'game': 'c9ab9cba-807d-4b83-82de-211d010bd3ba'}, {'game': 'c9c28db5-efbb-4015-89ce-dda4595a0e27'}, {'game': 'c9e8a840-dc72-4bc2-913a-d8156b600e21'}, {'game': 'cac87187-e919-46d6-a08d-e4ae79b8ea03'}, {'game': 'cb7f8f8b-eb36-4b45-9b74-5cac523fe42c'}, {'game': 'cbcf5f32-5928-4998-9728-dcce693ab6d5'}, {'game': 'cc877d12-301b-4207-b0fa-17cde0f81283'}, {'game': 'ccf2abac-73e0-4a91-ae16-92859478a33c'}, {'game': 'ccf9d687-2d2d-4980-b9a5-72879318d3dd'}, {'game': 'cd03f834-3448-4ace-9ce8-935c23492c92'}, {'game': 'cd307180-b75b-4cd2-ace7-fa2fea3098da'}, {'game': 'cdc88e02-9c15-4950-b372-a82c017a0381'}, {'game': 'ce05aa10-a889-4b51-9e3b-f489ac608a9b'}, {'game': 'ce410b6c-48a8-4298-9135-d993162289e4'}, {'game': 'cf074ff6-a1d0-4d76-96e9-38ff3cbb3f65'}, {'game': 'cf282793-06df-4960-a813-0bfee3ce4881'}, {'game': 'cf62db3a-0350-4efd-a370-1627c4e49d55'}, {'game': 'cf8f03ba-4268-4b59-b394-b00f0cf99601'}, {'game': 'd06ca0d8-ca7e-4792-b14f-37a213152e32'}, {'game': 'd2016b12-2eff-43e9-86a8-bf97d9a436c2'}, {'game': 'd21ec92b-eae6-4993-af67-2d78db00b767'}, {'game': 'd28f04f8-8fe0-43af-92f8-b57606a46137'}, {'game': 'd2d988d1-d095-4ea2-b19a-41b13229211c'}, {'game': 'd345f682-0e7f-42d2-a829-30cdc416fee9'}, {'game': 'd359385c-9db4-4965-bb2f-538774f609ff'}, {'game': 'd367f4f0-b903-4673-963d-6e7f97242af9'}, {'game': 'd42d223d-af5c-45e1-98ed-b6ab1c0da1d8'}, {'game': 'd587d449-be51-43aa-87a7-8923bd41b49c'}, {'game': 'd5cc73d9-eddf-4aad-b66b-188e28769cae'}, {'game': 'd61952e3-c3c1-45b3-8dcf-d9c872dd6107'}, {'game': 'd6547f29-48c3-460f-a318-eaf76fba9060'}, {'game': 'd712741e-b2ed-4c21-956f-34549907b315'}, {'game': 'd796a132-f5a3-4c46-b07b-e1c9d89f9d89'}, {'game': 'd822823f-ec34-4263-a66c-f0cc7ce244d9'}, {'game': 'd8ac1db3-9ac4-4ff2-bd1c-b04e979d5d0c'}, {'game': 'd9434aeb-4695-49e2-a90a-6c1bd8fd4fa3'}, {'game': 'd9f4395f-1434-4ff7-b0ac-dde4c692a439'}, {'game': 'da0d43ac-0061-4d1f-94db-cb5962b1f80a'}, {'game': 'daf32d92-4cc1-4c10-8411-42d13ad46ebe'}, {'game': 'db6bb94f-eaa7-49a2-9fec-507caa1d5eb1'}, {'game': 'dc6d73ac-7236-4740-93c3-dbaa9c3bd183'}, {'game': 'dc7280e7-1ccd-4ffe-9361-55cd72c7f867'}, {'game': 'dcb81c0a-e8e9-4305-b0e5-4f8b4432c24d'}, {'game': 'dcc0642c-3180-4f9e-954c-08ede78ec1b1'}, {'game': 'ddd3e542-773b-4a89-adf5-397b6c378f68'}, {'game': 'deed93ce-a307-4234-a000-1e29922fdea1'}, {'game': 'e22d59fd-c342-4c38-9bf8-3dd99530eb40'}, {'game': 'e2526528-b626-489f-9f47-43117005da72'}, {'game': 'e2765fe7-728a-4ee1-a694-38a54f7a71fe'}, {'game': 'e39d2115-1e1a-41aa-b209-fec43060cbc1'}, {'game': 'e3e66a47-a9e1-43c5-8c53-654e463fdc10'}, {'game': 'e421b8d2-22c6-45db-8933-97d683fd7b36'}, {'game': 'e4fe79c5-39e5-4fb6-bcb9-8ce75467d130'}, {'game': 'e5734c3c-de2d-491a-9a89-3c42034a16eb'}, {'game': 'e6bc9747-6b5e-46dc-a550-b5a7366c178c'}, {'game': 'e717a855-67f4-4fb6-b0d6-b13d7b0de0fc'}, {'game': 'e7ce3ae3-3590-40bb-b749-64af37d24696'}, {'game': 'e92c7c03-9575-485e-ad9b-5491b510f6b6'}, {'game': 'e962ddd6-8c21-40bc-bf07-f4c4d172517e'}, {'game': 'e9962b31-da7e-4878-8a7f-4532c50d22b5'}, {'game': 'e9ce5399-2815-40cd-8301-f5ab4e021abc'}, {'game': 'e9f3da8d-fb4c-4129-9bae-be927a3075f4'}, {'game': 'ea89e731-ea54-4bc0-898d-aca08e57998a'}, {'game': 'ebd25e89-6c07-42e4-bc1e-b6d1f79f8aea'}, {'game': 'ec32715d-3efa-4fec-9039-82d12ade4fb4'}, {'game': 'ec4d4d06-7279-45b5-9e06-081ffa399f47'}, {'game': 'ec50fc2f-b38f-4f1a-a2a4-656f486d4bb3'}, {'game': 'ece5a955-5361-4d2e-a896-2b65b78c106e'}, {'game': 'ede20ffe-8ddf-4eb2-a3d4-61eee39de75c'}, {'game': 'ee8a838b-0fa5-4c3c-8ebd-9f8f981f9a74'}, {'game': 'ef3a36e0-8f82-46a7-b026-eea4ffa963f0'}, {'game': 'ef650948-05f7-428d-956b-d805a3443aff'}, {'game': 'effb2494-9443-4c22-a2e5-32af9e90b76a'}, {'game': 'f0050663-1ebd-4392-a1ea-2aa5dc3d0e27'}, {'game': 'f09c78ff-de63-4494-86b1-770bd805c320'}, {'game': 'f0b7b7dc-8879-4059-9bb9-89573721ff35'}, {'game': 'f23ba2ed-fe7d-4358-b50a-92016b07013c'}, {'game': 'f2ab4a5f-c904-4d45-b186-f5f7fc476f12'}, {'game': 'f37fa400-e844-4571-bac3-1f717e527279'}, {'game': 'f3b045e4-632d-4244-add1-d51f54605021'}, {'game': 'f3f15375-ed5d-4360-a6f4-b8238b6fa4b3'}, {'game': 'f6a3033d-0d81-4001-b0e2-44e9211dbc25'}, {'game': 'f7453570-d6c3-4696-9190-c07800178603'}, {'game': 'f78652fc-33cf-4168-a101-98ab45cfd18d'}, {'game': 'f960f2a5-1f1d-484f-bf94-dab983609b89'}, {'game': 'fa3a0045-f0b5-4722-b8e6-8245fea8e0b9'}, {'game': 'fb4825bc-7101-49ac-ab88-e6304938bd16'}, {'game': 'fbaf2f69-c067-4f4a-a4f3-ae8b5ebf53b8'}, {'game': 'fbb39b21-e650-4cce-98ad-4ec443d40c55'}, {'game': 'fd600eff-3f44-4bae-a910-ad9d3bcea2f5'}, {'game': 'fe099815-b382-4b5c-b78a-275223c20f9c'}, {'game': 'fe1dc7e3-e6ab-4962-87e6-40f87682879c'}, {'game': 'fe752ac4-bdf7-4770-8f0e-f6ccf7e4d781'}, {'game': 'fec5a27a-0b21-49fc-8053-81dbe4a7e5e6'}, {'game': 'fedecd4e-ab6c-4e5c-b5a8-415ddbaed965'}], '_id': 'cGFyZW50X2FwaV9faWRzY2hlZHVsZV9wcmVsZWFndWVfX2lkMmZhNDQ4YmMtZmMxNy00ZDNkLWJlMDMtZTYwZTA4MGZkYzI2aWQ5NTIzZjAzOS0wNzBjLTQ5ZDEtYjJlMy01ZjE4YjU3YzVlZTM=', 'id': '9523f039-070c-49d1-b2e3-5f18b57c5ee3', 'dd_updated__id': 1454273951666, 'parent_api__id': 'schedule_pre', 'type': 'PRE'}"""
        self.season_parser = SeasonSchedule()

    def __validate_season(self, season_model, expected_season_year, expected_season_type):
        self.assertEquals(season_model.season_year, expected_season_year)
        self.assertEquals(season_model.season_type, expected_season_type)

    def test_pst_season(self):
        obj = literal_eval(self.obj_str)
        srid = obj.get('id') # the srid will be found in the 'id' field
        oplog_obj = OpLogObjWrapper('mlb','season_schedule', obj)
        self.season_parser.parse( oplog_obj )
        season = sports.mlb.models.Season.objects.get(srid=srid)
        self.__validate_season( season, 2015, 'pre' )

class TestGameScheduleParser(AbstractTest):
    """
    tests sports.mlb.parser.GameSchedule -- the parser for sports.mlb.models.Game objects
    """

    def setUp(self):
        super().setUp()
        self.sport = 'mlb'
        self.season_str = """{'league__id': '2fa448bc-fc17-4d3d-be03-e60e080fdc26', 'year': 2015.0, 'games__list': [{'game': '00255f24-34b5-4808-84d9-863d40977685'}, {'game': '0044864e-8348-4b0b-a743-3544a2080ca8'}, {'game': 'ffed8d30-5f8c-4e98-9748-f6bc89c8165c'}], '_id': 'cGFyZW50X2FwaV9faWRzY2hlZHVsZV9yZWdsZWFndWVfX2lkMmZhNDQ4YmMtZmMxNy00ZDNkLWJlMDMtZTYwZTA4MGZkYzI2aWQ5NTIzZjAzOS0wNzBjLTQ5ZDEtYjJlMy01ZjE4YjU3YzVlZTM=', 'id': '9523f039-070c-49d1-b2e3-5f18b57c5ee3', 'dd_updated__id': 1454275473990, 'parent_api__id': 'schedule_reg', 'type': 'REG'}"""
        self.away_team_str = """{'market': 'Detroit', 'league__id': '2ea6efe7-2e21-4f29-80a2-0a24ad1f5f85', 'division__id': '255fadc6-367e-4238-8ece-d0cddabf7d72', '_id': 'cGFyZW50X2FwaV9faWRoaWVyYXJjaHlsZWFndWVfX2lkMmVhNmVmZTctMmUyMS00ZjI5LTgwYTItMGEyNGFkMWY1Zjg1ZGl2aXNpb25fX2lkMjU1ZmFkYzYtMzY3ZS00MjM4LThlY2UtZDBjZGRhYmY3ZDcyaWQ1NzVjMTliNy00MDUyLTQxYzItOWYwYS0xYzU4MTNkMDJmOTk=', 'abbr': 'DET', 'id': '575c19b7-4052-41c2-9f0a-1c5813d02f99', 'dd_updated__id': 1456944323647, 'parent_api__id': 'hierarchy', 'venue': 'ef9a5eef-06c6-4963-ac70-7fd02c8c8d42', 'name': 'Tigers'}"""
        self.home_team_str = """{'market': 'Seattle', 'league__id': '2ea6efe7-2e21-4f29-80a2-0a24ad1f5f85', 'division__id': '59d3a9b1-30a8-4a6a-b4e6-0fe63257d01b', '_id': 'cGFyZW50X2FwaV9faWRoaWVyYXJjaHlsZWFndWVfX2lkMmVhNmVmZTctMmUyMS00ZjI5LTgwYTItMGEyNGFkMWY1Zjg1ZGl2aXNpb25fX2lkNTlkM2E5YjEtMzBhOC00YTZhLWI0ZTYtMGZlNjMyNTdkMDFiaWQ0M2EzOTA4MS01MmI0LTRmOTMtYWQyOS1kYTdmMzI5ZWE5NjA=', 'abbr': 'SEA', 'id': '43a39081-52b4-4f93-ad29-da7f329ea960', 'dd_updated__id': 1456944323647, 'parent_api__id': 'hierarchy', 'venue': 'f1c03dac-3c0f-437c-a325-8d5702cd321a', 'name': 'Mariners'}"""
        self.game_str = """{'home_team': '43a39081-52b4-4f93-ad29-da7f329ea960', 'league__id': '2fa448bc-fc17-4d3d-be03-e60e080fdc26', 'attendance': 22580.0, 'parent_list__id': 'games__list', 'parent_api__id': 'schedule_reg', 'venue': 'f1c03dac-3c0f-437c-a325-8d5702cd321a', 'dd_updated__id': 1454275473990, 'game_number': 1.0, 'coverage': 'full', 'season_schedule__id': '9523f039-070c-49d1-b2e3-5f18b57c5ee3', 'away': '575c19b7-4052-41c2-9f0a-1c5813d02f99', 'home': '43a39081-52b4-4f93-ad29-da7f329ea960', 'scheduled': '2015-07-07T02:10:00+00:00', 'status': 'closed', '_id': 'cGFyZW50X2FwaV9faWRzY2hlZHVsZV9yZWdsZWFndWVfX2lkMmZhNDQ4YmMtZmMxNy00ZDNkLWJlMDMtZTYwZTA4MGZkYzI2c2Vhc29uLXNjaGVkdWxlX19pZDk1MjNmMDM5LTA3MGMtNDlkMS1iMmUzLTVmMThiNTdjNWVlM3BhcmVudF9saXN0X19pZGdhbWVzX19saXN0aWQwMDQ0ODY0ZS04MzQ4LTRiMGItYTc0My0zNTQ0YTIwODBjYTg=', 'id': '0044864e-8348-4b0b-a743-3544a2080ca8', 'away_team': '575c19b7-4052-41c2-9f0a-1c5813d02f99', 'broadcast__list': {'network': 'ROOT SPORTS'}, 'day_night': 'N'}"""

        self.season_parser = SeasonSchedule()
        self.away_team_parser = TeamHierarchy()
        self.home_team_parser = TeamHierarchy()
        self.game_parser = GameSchedule()

    def test_game_schedule_parse(self):
        """
        as a prerequisite, parse the seasonschedule, and both home & away teams

        effectively tests the TeamHierarchy parser too
        """
        # parse the season_schedule obj
        season_oplog_obj = OpLogObjWrapper(self.sport,'season_schedule',literal_eval(self.season_str))
        self.season_parser.parse( season_oplog_obj )
        self.assertEquals( 1, sports.mlb.models.Season.objects.filter(season_year=2015,season_type='reg').count() ) # should have parsed 1 thing

        away_team_oplog_obj = OpLogObjWrapper(self.sport,'team',literal_eval(self.away_team_str))
        self.away_team_parser.parse( away_team_oplog_obj )
        self.assertEquals( 1, sports.mlb.models.Team.objects.all().count() ) # should be 1 team in there now

        home_team_oplog_obj = OpLogObjWrapper(self.sport,'team',literal_eval(self.home_team_str))
        self.home_team_parser.parse( home_team_oplog_obj )
        self.assertEquals( 2, sports.mlb.models.Team.objects.all().count() ) # should be 2 teams in there now

        # now attempt to parse the game
        game_oplog_obj = OpLogObjWrapper(self.sport,'game',literal_eval(self.game_str))
        self.game_parser.parse( game_oplog_obj )
        self.assertEquals( 1, sports.mlb.models.Game.objects.all().count() )

class QuickCacheAndReqTest(AbstractTest):

    def setUp(self):
        super().setUp()

    def test_1(self):
        pitcher = {"pitcher_hand": "R", "pitch_zone": 12.0, "pitch_type": "CU", "dd_updated__id": 1469497407373,
                   "pitch_speed": 82.0, "pitch__id": "c8f11efb-9edd-4653-9b8a-617fb9650b30",
                   "at_bat__id": "71f664ce-5bbb-46fa-9ede-c5136befed3c",
                   "game__id": "dcb8bf15-fdce-4813-b9f6-da00fcd258cd", "parent_api__id": "pbp", "hitter_hand": "R",
                   "_id": "cGFyZW50X2FwaV9faWRwYnBnYW1lX19pZGRjYjhiZjE1LWZkY2UtNDgxMy1iOWY2LWRhMDBmY2QyNThjZGF0X2JhdF9faWQ3MWY2NjRjZS01YmJiLTQ2ZmEtOWVkZS1jNTEzNmJlZmVkM2NwaXRjaF9faWRjOGYxMWVmYi05ZWRkLTQ2NTMtOWI4YS02MTdmYjk2NTBiMzBpZDUxMDZjNzQ5LTQxODUtNDM4Zi1iN2IyLTAxOThiMTRhNTdjYg==",
                   "id": "5106c749-4185-438f-b7b2-0198b14a57cb", "pitch_count": 13.0}

        c = PitcherCache(pitcher)
        self.assertIsNotNone(c.fetch(1469497407373, "c8f11efb-9edd-4653-9b8a-617fb9650b30"))

class PbpParserTest(AbstractTest):

    def setUp(self):
        super().setUp()
        self.parser = PbpParser()

    def __parse_and_send(self, unwrapped_obj, target):
        parts = target[0].split('.')
        oplog_obj = OpLogObjWrapper(parts[0], parts[1], unwrapped_obj)
        self.parser.parse(oplog_obj, target=target)

    def test_1(self):
        """
        test xander bogaerts at bat

            per espn, the whole inning went:
                Sandy Leon	Ball, León (singled)
                Brock Holt	Strike (looking), (popped out)
                Mookie Betts	Strike (looking), Strike (looking), Betts (fouled out)
                Dustin Pedroia	Ball, Ball, Ball, Strike (looking), Ball, (walked, Leon to second)
                Xander Bogaerts	Ball, Ball, Strike (looking), Strike (foul) (popped out to shortstop)

        """
        sport_db = 'mlb'
        parent_api = 'pbp'

        pitcher = {"pitcher_hand": "R", "pitch_zone": 12.0, "pitch_type": "CU", "dd_updated__id": 1469497407373,
                   "pitch_speed": 82.0, "pitch__id": "c8f11efb-9edd-4653-9b8a-617fb9650b30",
                   "at_bat__id": "71f664ce-5bbb-46fa-9ede-c5136befed3c",
                   "game__id": "dcb8bf15-fdce-4813-b9f6-da00fcd258cd", "parent_api__id": "pbp", "hitter_hand": "R",
                   "_id": "cGFyZW50X2FwaV9faWRwYnBnYW1lX19pZGRjYjhiZjE1LWZkY2UtNDgxMy1iOWY2LWRhMDBmY2QyNThjZGF0X2JhdF9faWQ3MWY2NjRjZS01YmJiLTQ2ZmEtOWVkZS1jNTEzNmJlZmVkM2NwaXRjaF9faWRjOGYxMWVmYi05ZWRkLTQ2NTMtOWI4YS02MTdmYjk2NTBiMzBpZDUxMDZjNzQ5LTQxODUtNDM4Zi1iN2IyLTAxOThiMTRhNTdjYg==",
                   "id": "5106c749-4185-438f-b7b2-0198b14a57cb", "pitch_count": 13.0}
        self.__parse_and_send(pitcher, (sport_db + '.' + 'pitcher', parent_api))

        runner = {"parent_list__id": "runners__list", "first_name": "Dustin", "out": "false",
                  "dd_updated__id": 1469497407373, "at_bat__id": "71f664ce-5bbb-46fa-9ede-c5136befed3c",
                  "jersey_number": 15.0, "pitch__id": "c8f11efb-9edd-4653-9b8a-617fb9650b30",
                  "_id": "cGFyZW50X2FwaV9faWRwYnBnYW1lX19pZGRjYjhiZjE1LWZkY2UtNDgxMy1iOWY2LWRhMDBmY2QyNThjZGF0X2JhdF9faWQ3MWY2NjRjZS01YmJiLTQ2ZmEtOWVkZS1jNTEzNmJlZmVkM2NwaXRjaF9faWRjOGYxMWVmYi05ZWRkLTQ2NTMtOWI4YS02MTdmYjk2NTBiMzBwYXJlbnRfbGlzdF9faWRydW5uZXJzX19saXN0aWQ0MDA4NWMwNS1mYTA2LTRlZWMtOWY0MS1mMDI0NTk4MGY2YTA=",
                  "parent_api__id": "pbp", "ending_base": 1.0, "game__id": "dcb8bf15-fdce-4813-b9f6-da00fcd258cd",
                  "id": "40085c05-fa06-4eec-9f41-f0245980f6a0", "last_name": "Pedroia", "preferred_name": "Dustin",
                  "starting_base": 1.0}
        self.__parse_and_send(runner, (sport_db + '.' + 'runner', parent_api))

        at_bat = {"hitter_id": "272abdba-ae99-4137-a6dd-5615f234adfc", "pitch": "c8f11efb-9edd-4653-9b8a-617fb9650b30",
                  "game__id": "dcb8bf15-fdce-4813-b9f6-da00fcd258cd", "id": "71f664ce-5bbb-46fa-9ede-c5136befed3c",
                  "_id": "cGFyZW50X2FwaV9faWRwYnBnYW1lX19pZGRjYjhiZjE1LWZkY2UtNDgxMy1iOWY2LWRhMDBmY2QyNThjZGlkNzFmNjY0Y2UtNWJiYi00NmZhLTllZGUtYzUxMzZiZWZlZDNj",
                  "parent_api__id": "pbp", "dd_updated__id": 1469497407373}
        self.__parse_and_send(at_bat, (sport_db + '.' + 'at_bat', parent_api))

        runner = {"first_name": "Sandy", "starting_base": 2.0, "parent_api__id": "pbp", "jersey_number": 3.0,
                  "ending_base": 2.0, "at_bat__id": "71f664ce-5bbb-46fa-9ede-c5136befed3c",
                  "_id": "cGFyZW50X2FwaV9faWRwYnBnYW1lX19pZGRjYjhiZjE1LWZkY2UtNDgxMy1iOWY2LWRhMDBmY2QyNThjZGF0X2JhdF9faWQ3MWY2NjRjZS01YmJiLTQ2ZmEtOWVkZS1jNTEzNmJlZmVkM2NwaXRjaF9faWRjOGYxMWVmYi05ZWRkLTQ2NTMtOWI4YS02MTdmYjk2NTBiMzBwYXJlbnRfbGlzdF9faWRydW5uZXJzX19saXN0aWQyNGQwNTdhOS00ZGVmLTRlOWUtYmU4My0zZWNhMDFjOWM5MjI=",
                  "last_name": "Leon", "dd_updated__id": 1469497407373, "preferred_name": "Sandy",
                  "id": "24d057a9-4def-4e9e-be83-3eca01c9c922", "pitch__id": "c8f11efb-9edd-4653-9b8a-617fb9650b30",
                  "game__id": "dcb8bf15-fdce-4813-b9f6-da00fcd258cd", "parent_list__id": "runners__list",
                  "out": "false"}
        self.__parse_and_send(runner, (sport_db + '.' + 'runner', parent_api))

        pitch = {"at_bat__id": "71f664ce-5bbb-46fa-9ede-c5136befed3c", "updated_at": "2016-07-26T01:43:19Z",
                 "runners__list": [{"runner": "40085c05-fa06-4eec-9f41-f0245980f6a0"},
                                   {"runner": "24d057a9-4def-4e9e-be83-3eca01c9c922"}], "outcome_id": "bB",
                 "flags__list": {"is_double_play": "false", "is_wild_pitch": "false", "is_hit": "false",
                                 "is_triple_play": "false", "is_bunt_shown": "false", "is_ab": "false",
                                 "is_passed_ball": "false", "is_on_base": "false", "is_bunt": "false",
                                 "is_ab_over": "false"}, "game__id": "dcb8bf15-fdce-4813-b9f6-da00fcd258cd",
                 "dd_updated__id": 1469497407373, "status": "official",
                 "count__list": {"pitch_count": 1.0, "balls": 1.0, "outs": 2.0, "strikes": 0.0},
                 "pitcher": "5106c749-4185-438f-b7b2-0198b14a57cb",
                 "_id": "cGFyZW50X2FwaV9faWRwYnBnYW1lX19pZGRjYjhiZjE1LWZkY2UtNDgxMy1iOWY2LWRhMDBmY2QyNThjZGF0X2JhdF9faWQ3MWY2NjRjZS01YmJiLTQ2ZmEtOWVkZS1jNTEzNmJlZmVkM2NpZGM4ZjExZWZiLTllZGQtNDY1My05YjhhLTYxN2ZiOTY1MGIzMA==",
                 "id": "c8f11efb-9edd-4653-9b8a-617fb9650b30", "created_at": "2016-07-26T01:43:16Z",
                 "parent_api__id": "pbp"}
        self.__parse_and_send(pitch, (sport_db + '.' + 'pitch', parent_api))

    def test_2(self):
        """ test with a base runner """
        sport_db = 'mlb'
        parent_api = 'pbp'

        # zone pitch 1 came in before the rest of the data (based on its dd_updated__id)
        pitcher = {
            "_id": "cGFyZW50X2FwaV9faWRwYnBnYW1lX19pZGQyYjRlNWFlLTRiYTQtNDJiYS05NTA5LTc0YTBjNjdhZWZlYmF0X2JhdF9faWRiZmVjZjI3NC1jMTU1LTQ2YmItODAwOC0yYTk5NjhmZjliODhwaXRjaF9faWRkZmI2ZTIwZS02OTJjLTRmNDEtOGIwNi04MjFlYzc0N2JmYmNpZDlmYjE4ODM4LTZhYzgtNDNiNi1iYmRkLTY5ZjlmOGE5ODNhYw==",
            "pitch__id": "dfb6e20e-692c-4f41-8b06-821ec747bfbc", "dd_updated__id": 1469637786169,
            "id": "9fb18838-6ac8-43b6-bbdd-69f9f8a983ac", "pitcher_hand": "R", "parent_api__id": "pbp",
            "game__id": "d2b4e5ae-4ba4-42ba-9509-74a0c67aefeb", "at_bat__id": "bfecf274-c155-46bb-8008-2a9968ff9b88",
            "hitter_hand": "R", "pitch_count": 12.0, "pitch_zone": 1.0, "pitch_speed":94.0}
        self.__parse_and_send(pitcher, (sport_db + '.' + 'pitcher', parent_api))

        # zone pitch 2
        pitcher = {"at_bat__id": "bfecf274-c155-46bb-8008-2a9968ff9b88", "parent_api__id": "pbp", "pitch_count": 13.0,
                   "_id": "cGFyZW50X2FwaV9faWRwYnBnYW1lX19pZGQyYjRlNWFlLTRiYTQtNDJiYS05NTA5LTc0YTBjNjdhZWZlYmF0X2JhdF9faWRiZmVjZjI3NC1jMTU1LTQ2YmItODAwOC0yYTk5NjhmZjliODhwaXRjaF9faWRhYmY2NTBhMy1jMGYwLTQ5MzYtYTIxNi04MTk2ZTAwMDMxZGZpZDlmYjE4ODM4LTZhYzgtNDNiNi1iYmRkLTY5ZjlmOGE5ODNhYw==",
                   "pitch__id": "abf650a3-c0f0-4936-a216-8196e00031df", "dd_updated__id": 1469637804257,
                   "hitter_hand": "R", "game__id": "d2b4e5ae-4ba4-42ba-9509-74a0c67aefeb",
                   "id": "9fb18838-6ac8-43b6-bbdd-69f9f8a983ac", "pitcher_hand": "R", "pitch_zone": 1.0, "pitch_speed":94.0}
        self.__parse_and_send(pitcher, (sport_db + '.' + 'pitcher', parent_api))

        at_bat = {"steal": "4f83cbab-526f-46e5-8d54-39c77b8afb0f", "dd_updated__id": 1469637804257,
                  "hitter_id": "f4c666e5-2a05-4258-8ddc-da6e0cffdb57", "id": "bfecf274-c155-46bb-8008-2a9968ff9b88",
                  "parent_api__id": "pbp",
                  "_id": "cGFyZW50X2FwaV9faWRwYnBnYW1lX19pZGQyYjRlNWFlLTRiYTQtNDJiYS05NTA5LTc0YTBjNjdhZWZlYmlkYmZlY2YyNzQtYzE1NS00NmJiLTgwMDgtMmE5OTY4ZmY5Yjg4",
                  "pitchs": [{"pitch": "dfb6e20e-692c-4f41-8b06-821ec747bfbc"},
                             {"pitch": "abf650a3-c0f0-4936-a216-8196e00031df"}],
                  "game__id": "d2b4e5ae-4ba4-42ba-9509-74a0c67aefeb"}
        self.__parse_and_send(at_bat, (sport_db + '.' + 'at_bat', parent_api))

        runner = {"jersey_number": 4.0, "parent_api__id": "pbp", "id": "8f6f5bdf-9712-472e-8af5-12d5fb1e52e8",
                  "at_bat__id": "bfecf274-c155-46bb-8008-2a9968ff9b88", "out": "false", "first_name": "William",
                  "_id": "cGFyZW50X2FwaV9faWRwYnBnYW1lX19pZGQyYjRlNWFlLTRiYTQtNDJiYS05NTA5LTc0YTBjNjdhZWZlYmF0X2JhdF9faWRiZmVjZjI3NC1jMTU1LTQ2YmItODAwOC0yYTk5NjhmZjliODhwaXRjaF9faWRhYmY2NTBhMy1jMGYwLTQ5MzYtYTIxNi04MTk2ZTAwMDMxZGZwYXJlbnRfbGlzdF9faWRydW5uZXJzX19saXN0aWQ4ZjZmNWJkZi05NzEyLTQ3MmUtOGFmNS0xMmQ1ZmIxZTUyZTg=",
                  "pitch__id": "abf650a3-c0f0-4936-a216-8196e00031df", "dd_updated__id": 1469637804257,
                  "starting_base": 1.0, "last_name": "Myers", "preferred_name": "Wil", "ending_base": 1.0,
                  "game__id": "d2b4e5ae-4ba4-42ba-9509-74a0c67aefeb", "parent_list__id": "runners__list"}
        self.__parse_and_send(runner, (sport_db + '.' + 'runner', parent_api))

        pitch = {"id": "abf650a3-c0f0-4936-a216-8196e00031df",
                 "flags__list": {"is_on_base": "false", "is_wild_pitch": "false", "is_hit": "false", "is_bunt": "false",
                                 "is_ab": "false", "is_bunt_shown": "false", "is_triple_play": "false",
                                 "is_double_play": "false", "is_passed_ball": "false", "is_ab_over": "false"},
                 "pitcher": "9fb18838-6ac8-43b6-bbdd-69f9f8a983ac",
                 "count__list": {"balls": 0.0, "strikes": 2.0, "outs": 1.0, "pitch_count": 2.0},
                 "_id": "cGFyZW50X2FwaV9faWRwYnBnYW1lX19pZGQyYjRlNWFlLTRiYTQtNDJiYS05NTA5LTc0YTBjNjdhZWZlYmF0X2JhdF9faWRiZmVjZjI3NC1jMTU1LTQ2YmItODAwOC0yYTk5NjhmZjliODhpZGFiZjY1MGEzLWMwZjAtNDkzNi1hMjE2LTgxOTZlMDAwMzFkZg==",
                 "status": "official", "runners__list": {"runner": "8f6f5bdf-9712-472e-8af5-12d5fb1e52e8"},
                 "dd_updated__id": 1469637804257, "outcome_id": "kKL",
                 "at_bat__id": "bfecf274-c155-46bb-8008-2a9968ff9b88", "created_at": "2016-07-27T16:43:22Z",
                 "game__id": "d2b4e5ae-4ba4-42ba-9509-74a0c67aefeb", "parent_api__id": "pbp"}
        self.__parse_and_send(pitch, (sport_db + '.' + 'pitch', parent_api))