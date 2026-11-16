import json
import os
import urllib.parse

# 1. Complete Verified Live Public & Educational Free-to-Air Channels (30 channels)
LIVE_CHANNELS = [
    # Brasil (10 canais)
    {
        "id": "TVBrasil.br",
        "name": "TV Brasil (EBC)",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/Logotipo_da_TV_Brasil.svg/512px-Logotipo_da_TV_Brasil.svg.png",
        "ref_logo": "logos/tv_brasil.svg",
        "group": "Canais Públicos & Educativos (Ao Vivo)",
        "url": "https://tvbrasil-stream.ebc.com.br/index.m3u8",
        "country": "BR",
        "lang": "pt-BR",
        "desc": "Emissora pública da Empresa Brasil de Comunicação (EBC). Conteúdo cultural, educativo e jornalístico gratuito."
    },
    {
        "id": "CanalGov.br",
        "name": "Canal Gov (EBC)",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6a/Logotipo_do_Canal_Gov.svg/512px-Logotipo_do_Canal_Gov.svg.png",
        "ref_logo": "logos/canal_gov.svg",
        "group": "Canais Públicos & Educativos (Ao Vivo)",
        "url": "https://canalgov-stream.ebc.com.br/index.m3u8",
        "country": "BR",
        "lang": "pt-BR",
        "desc": "Canal de televisão governamental sob gestão da EBC. Transmissão pública de utilidade pública, atos institucionais e educação cívica."
    },
    {
        "id": "CulturaFast.br",
        "name": "TV Cultura",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/82/Logo_TV_Cultura_2020.svg/512px-Logo_TV_Cultura_2020.svg.png",
        "ref_logo": "logos/tv_cultura.svg",
        "group": "Canais Públicos & Educativos (Ao Vivo)",
        "url": "https://fpa-gateway.tvcultura.com.br:8181/memfs/606caef0-a290-413d-9f1f-8fcdb3a73831.m3u8",
        "country": "BR",
        "lang": "pt-BR",
        "desc": "Fundação Padre Anchieta. A mais premiada emissora educativa e cultural da televisão pública brasileira."
    },
    {
        "id": "TVSenado.br",
        "name": "TV Senado",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6e/TV_Senado_logo.svg/512px-TV_Senado_logo.svg.png",
        "ref_logo": "logos/tv_senado.svg",
        "group": "Canais Públicos & Educativos (Ao Vivo)",
        "url": "http://170.83.16.50/TV_SENADO/index.m3u8",
        "country": "BR",
        "lang": "pt-BR",
        "desc": "Canal legislativo oficial aberto do Senado Federal do Brasil. Transmissões de sessões, debates e documentários culturais."
    },
    {
        "id": "TVCamara.br",
        "name": "TV Câmara",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/07/Logo_TV_C%C3%A2mara.svg/512px-Logo_TV_C%C3%A2mara.svg.png",
        "ref_logo": "logos/tv_camara.svg",
        "group": "Canais Públicos & Educativos (Ao Vivo)",
        "url": "https://stream3.camara.gov.br/tv1/manifest.m3u8",
        "country": "BR",
        "lang": "pt-BR",
        "desc": "Canal oficial aberto da Câmara dos Deputados do Brasil. Plenário, comissões e programas culturais públicos."
    },
    {
        "id": "TVJustica.br",
        "name": "TV Justiça",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6b/Logo_TV_Justi%C3%A7a.png/512px-Logo_TV_Justi%C3%A7a.png",
        "ref_logo": "logos/tv_justica.svg",
        "group": "Canais Públicos & Educativos (Ao Vivo)",
        "url": "http://170.83.16.50/TV_JUSTICA/index.m3u8",
        "country": "BR",
        "lang": "pt-BR",
        "desc": "Canal público coordenado pelo Supremo Tribunal Federal (STF). Julgamentos ao vivo e debates jurídicos de utilidade pública."
    },
    {
        "id": "CanalEducacao.br",
        "name": "Canal Educação (MEC / EBC)",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c2/Canal_Educa%C3%A7%C3%A3o_logo_2023.png/512px-Canal_Educa%C3%A7%C3%A3o_logo_2023.png",
        "ref_logo": "logos/canal_educacao.svg",
        "group": "Canais Públicos & Educativos (Ao Vivo)",
        "url": "https://canaleducacao-stream.ebc.com.br/index.m3u8",
        "country": "BR",
        "lang": "pt-BR",
        "desc": "Canal oficial educativo do Ministério da Educação (MEC) gerido pela EBC."
    },
    {
        "id": "CanalFutura.br",
        "name": "Canal Futura",
        "logo": "https://upload.wikimedia.org/wikipedia/pt/thumb/d/d4/Logotipo_do_Canal_Futura.png/512px-Logotipo_do_Canal_Futura.png",
        "ref_logo": "logos/canal_futura.svg",
        "group": "Canais Públicos & Educativos (Ao Vivo)",
        "url": "http://170.83.16.50/FUTURA/index.m3u8",
        "country": "BR",
        "lang": "pt-BR",
        "desc": "Projeto de comunicação comunitária e educativa pioneiro no Brasil."
    },
    {
        "id": "TVEBahia.br",
        "name": "TVE Bahia (IRDEB)",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/05/Logo_TVE_Bahia_2017.png/512px-Logo_TVE_Bahia_2017.png",
        "ref_logo": "logos/tve_bahia.svg",
        "group": "Canais Públicos & Educativos (Ao Vivo)",
        "url": "http://streaming.procergs.com.br:1935/tve/stve/playlist.m3u8",
        "country": "BR",
        "lang": "pt-BR",
        "desc": "Emissora pública educativa do Instituto de Radiodifusão Educativa da Bahia."
    },
    {
        "id": "CulturaPara.br",
        "name": "TV Cultura do Pará (FUNTELPA)",
        "logo": "https://upload.wikimedia.org/wikipedia/pt/thumb/9/90/TV_Cultura_do_Par%C3%A1_logo.png/512px-TV_Cultura_do_Par%C3%A1_logo.png",
        "ref_logo": "logos/cultura_para.svg",
        "group": "Canais Públicos & Educativos (Ao Vivo)",
        "url": "http://www.portalcultura.com.br/playerhtml/funtelpa/tv_funtelpa/playlist.m3u8",
        "country": "BR",
        "lang": "pt-BR",
        "desc": "Fundação Paraense de Radiodifusão (FUNTELPA). Emissora pública e cultural do Pará."
    },

    # Portugal & Europa (6 canais)
    {
        "id": "ARTV.pt",
        "name": "ARTV - Canal Parlamento (Portugal)",
        "logo": "https://upload.wikimedia.org/wikipedia/pt/thumb/2/29/Canal_Parlamento.png/512px-Canal_Parlamento.png",
        "ref_logo": "logos/artv_portugal.svg",
        "group": "Canais Públicos & Educativos (Ao Vivo)",
        "url": "https://playout172.livextend.cloud/liveiframe/_definst_/liveartvabr/playlist.m3u8",
        "country": "PT",
        "lang": "pt-PT",
        "desc": "Canal oficial de transmissão pública da Assembleia da República de Portugal."
    },
    {
        "id": "EuronewsPortuguese.fr",
        "name": "Euronews (Edição em Português)",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/00/Euronews_logo_2016.svg/512px-Euronews_logo_2016.svg.png",
        "ref_logo": "logos/euronews_pt.svg",
        "group": "Canais Públicos & Educativos (Ao Vivo)",
        "url": "https://cdn-euronews.akamaized.net/live/eds/euronews-pt/25040/index.m3u8",
        "country": "EU",
        "lang": "pt",
        "desc": "Sinal internacional de notícias pan-europeu gratuito e aberto com locução em português."
    },
    {
        "id": "CanalParlamento.es",
        "name": "Canal Parlamento (Espanha)",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/Logo_Congreso_de_los_Diputados.svg/512px-Logo_Congreso_de_los_Diputados.svg.png",
        "ref_logo": "logos/canal_parlamento_es.svg",
        "group": "Canais Públicos & Educativos (Ao Vivo)",
        "url": "https://congresodirecto.akamaized.net/hls/live/2037973/canalparlamento/master.m3u8",
        "country": "ES",
        "lang": "es",
        "desc": "Emissão oficial aberta do Congresso dos Deputados do Reino de Espanha."
    },
    {
        "id": "ARDalpha.de",
        "name": "ARD-alpha (Alemanha)",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/87/ARD-alpha_2019.svg/512px-ARD-alpha_2019.svg.png",
        "ref_logo": "logos/ard_alpha.svg",
        "group": "Canais Públicos & Educativos (Ao Vivo)",
        "url": "https://mcdn.br.de/br/fs/ard_alpha/hls/de/master.m3u8",
        "country": "DE",
        "lang": "de",
        "desc": "O canal de televisão público alemão de ciência, educação e alta cultura da rede ARD."
    },
    {
        "id": "SenatoTV.it",
        "name": "Senato TV (Itália)",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/36/Logo_Senato_della_Repubblica.svg/512px-Logo_Senato_della_Repubblica.svg.png",
        "ref_logo": "logos/senato_tv_it.svg",
        "group": "Canais Públicos & Educativos (Ao Vivo)",
        "url": "https://senato-live.morescreens.com/SENATO_1_001/playlist.m3u8",
        "country": "IT",
        "lang": "it",
        "desc": "Transmissão parlamentar oficial aberta do Senado da República Italiana."
    },
    {
        "id": "CameradeiDeputati.it",
        "name": "Camera dei Deputati (Itália)",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/32/Emblem_of_the_Chamber_of_Deputies_%28Italy%29.svg/512px-Emblem_of_the_Chamber_of_Deputies_%28Italy%29.svg.png",
        "ref_logo": "logos/camera_deputati_it.svg",
        "group": "Canais Públicos & Educativos (Ao Vivo)",
        "url": "https://video-ar.radioradicale.it/diretta/camera2/playlist.m3u8",
        "country": "IT",
        "lang": "it",
        "desc": "Transmissão oficial ao vivo da Câmara dos Deputados do Parlamento Italiano."
    },

    # América Latina (7 canais)
    {
        "id": "SenalColombia.co",
        "name": "Señal Colombia",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8e/Se%C3%B1al_Colombia_logo.svg/512px-Se%C3%B1al_Colombia_logo.svg.png",
        "ref_logo": "logos/senal_colombia.svg",
        "group": "Canais Públicos & Educativos (Ao Vivo)",
        "url": "http://138.121.15.230:9002/SENAL-COLOMBIA/index.m3u8",
        "country": "CO",
        "lang": "es",
        "desc": "Emissora de televisão pública nacional educativa e cultural da Colômbia (RTVC)."
    },
    {
        "id": "CanalInstitucional.co",
        "name": "Canal Institucional (Colômbia)",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/Canal_Institucional_logo_2018.png/512px-Canal_Institucional_logo_2018.png",
        "ref_logo": "logos/canal_institucional_co.svg",
        "group": "Canais Públicos & Educativos (Ao Vivo)",
        "url": "http://190.61.47.54:8000/play/a00v/index.m3u8",
        "country": "CO",
        "lang": "es",
        "desc": "Canal estatal da Colômbia dedicado a informar a cidadania sobre o Estado e serviços públicos."
    },
    {
        "id": "CanalCongreso.co",
        "name": "Canal Congreso (Colômbia)",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/91/Logo_del_Congreso_de_la_Rep%C3%BAblica_de_Colombia.png/512px-Logo_del_Congreso_de_la_Rep%C3%BAblica_de_Colombia.png",
        "ref_logo": "logos/canal_congreso_co.svg",
        "group": "Canais Públicos & Educativos (Ao Vivo)",
        "url": "http://138.121.15.230:9002/CANAL-CONGRESO/index.m3u8",
        "country": "CO",
        "lang": "es",
        "desc": "Canal institucional oficial do Congresso da República da Colômbia."
    },
    {
        "id": "TVSenado.cl",
        "name": "TV Senado (Chile)",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/18/Logo_Senado_de_Chile.svg/512px-Logo_Senado_de_Chile.svg.png",
        "ref_logo": "logos/tv_senado_cl.svg",
        "group": "Canais Públicos & Educativos (Ao Vivo)",
        "url": "https://janus-tv-ply.senado.cl/playlist/playlist.m3u8",
        "country": "CL",
        "lang": "es",
        "desc": "Canal oficial aberto de televisão do Senado da República do Chile."
    },
    {
        "id": "TVPeru.pe",
        "name": "TV Perú",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/16/TV_Per%C3%BA_logo_2019.png/512px-TV_Per%C3%BA_logo_2019.png",
        "ref_logo": "logos/tv_peru.svg",
        "group": "Canais Públicos & Educativos (Ao Vivo)",
        "url": "http://181.224.200.5:2277/play/a0dx/index.m3u8",
        "country": "PE",
        "lang": "es",
        "desc": "A mais antiga emissora pública do Peru, pertencente ao Instituto Nacional de Radio y Televisión."
    },
    {
        "id": "CanalIPe.pe",
        "name": "Canal IPe (Peru)",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7b/Canal_IPe_logo_2020.png/512px-Canal_IPe_logo_2020.png",
        "ref_logo": "logos/canal_ipe_pe.svg",
        "group": "Canais Públicos & Educativos (Ao Vivo)",
        "url": "http://187.102.210.46/IPE/index.m3u8",
        "country": "PE",
        "lang": "es",
        "desc": "Canal público cultural e infanto-juvenil do Ministério da Educação do Peru."
    },
    {
        "id": "Cultura24.pe",
        "name": "Cultura 24 (Peru)",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/cc/Escudo_nacional_del_Per%C3%BA.svg/512px-Escudo_nacional_del_Per%C3%BA.svg.png",
        "ref_logo": "logos/cultura_24_pe.svg",
        "group": "Canais Públicos & Educativos (Ao Vivo)",
        "url": "https://www.opencaster.com/resources/hls_stream/cultura24.m3u8",
        "country": "PE",
        "lang": "es",
        "desc": "Canal audiovisual oficial de difusão de patrimônio e artes do Ministério da Cultura do Peru."
    },

    # Estados Unidos & Organizações Globais (4 canais)
    {
        "id": "UNWebTV.us",
        "name": "UN Web TV (Nações Unidas)",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2f/Flag_of_the_United_Nations.svg/512px-Flag_of_the_United_Nations.svg.png",
        "ref_logo": "logos/un_web_tv.svg",
        "group": "Canais Públicos & Educativos (Ao Vivo)",
        "url": "https://cdnapi.kaltura.com/p/2503451/sp/250345100/playManifest/entryId/1_gb6tjmle/protocol/https/format/applehttp/a.m3u8",
        "country": "UN",
        "lang": "multilingual",
        "desc": "Canal oficial internacional da Organização das Nações Unidas (ONU) transmitindo assembleias e direitos humanos."
    },
    {
        "id": "ClassicArtsShowcase.us",
        "name": "Classic Arts Showcase",
        "logo": "https://upload.wikimedia.org/wikipedia/en/thumb/e/ec/Classic_Arts_Showcase_logo.png/512px-Classic_Arts_Showcase_logo.png",
        "ref_logo": "logos/classic_arts_showcase.svg",
        "group": "Canais Públicos & Educativos (Ao Vivo)",
        "url": "https://classicarts.akamaized.net/hls/live/1024257/CAS/master.m3u8",
        "country": "US",
        "lang": "en",
        "desc": "Canal 24/7 de fomento cultural gratuito: concertos clássicos, óperas, balés e acervos de domínio público."
    },
    {
        "id": "Create.us",
        "name": "Create TV (PBS)",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/90/Create_TV_logo.svg/512px-Create_TV_logo.svg.png",
        "ref_logo": "logos/create_tv.svg",
        "group": "Canais Públicos & Educativos (Ao Vivo)",
        "url": "https://create.lls.pbs.org/index.m3u8",
        "country": "US",
        "lang": "en",
        "desc": "Rede pública americana educativa (PBS) dedicada a artes, culinária, pintura e sustentabilidade."
    },
    {
        "id": "DistrictofColumbiaNetwork.us",
        "name": "DCN - District of Columbia Network",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d4/Flag_of_the_District_of_Columbia.svg/512px-Flag_of_the_District_of_Columbia.svg.png",
        "ref_logo": "logos/dcn_washington.svg",
        "group": "Canais Públicos & Educativos (Ao Vivo)",
        "url": "https://video.oct.dc.gov/out/u/DCN.m3u8",
        "country": "US",
        "lang": "en",
        "desc": "Canal público governamental e de transparência cívica da capital dos Estados Unidos (Washington D.C.)."
    },

    # Ásia & Internacional (3 canais)
    {
        "id": "NHKWorldJapan.jp",
        "name": "NHK World-Japan",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b3/NHK_World-Japan_logo_2020.svg/512px-NHK_World-Japan_logo_2020.svg.png",
        "ref_logo": "logos/nhk_world.svg",
        "group": "Canais Públicos & Educativos (Ao Vivo)",
        "url": "https://freem3u.xyz/api/live/play.m3u8?vid=106",
        "country": "JP",
        "lang": "en",
        "desc": "Transmissão internacional pública aberta do Japão (NHK) com notícias globais e documentários sobre ciência e cultura."
    },
    {
        "id": "KTV.kr",
        "name": "KTV - Korea Policy TV",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/09/Flag_of_South_Korea.svg/512px-Flag_of_South_Korea.svg.png",
        "ref_logo": "logos/ktv_korea.svg",
        "group": "Canais Públicos & Educativos (Ao Vivo)",
        "url": "https://hlive.ktv.go.kr/live/klive_h.stream/playlist.m3u8",
        "country": "KR",
        "lang": "ko",
        "desc": "Canal oficial público de políticas públicas, história nacional e cidadania da Coreia do Sul."
    },
    {
        "id": "ArirangTV.kr",
        "name": "Arirang TV",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1b/Arirang_TV_logo.svg/512px-Arirang_TV_logo.svg.png",
        "ref_logo": "logos/arirang_tv.svg",
        "group": "Canais Públicos & Educativos (Ao Vivo)",
        "url": "https://dash3.antik.sk/live/test_arirang/playlist.m3u8",
        "country": "KR",
        "lang": "en",
        "desc": "Emissora internacional pública em língua inglesa sediada em Seul, com foco em cultura, cooperação internacional e artes."
    }
]

# 2. Creative Commons Open Movies (Blender Foundation & Open Cinema)
OPEN_MOVIES = [
    {
        "id": "BigBuckBunny_2008",
        "title": "Big Buck Bunny",
        "year": 2008,
        "group": "Cinema Aberto & Creative Commons",
        "director": "Sacha Goedegebure (Blender Foundation)",
        "lang": "Sem Diálogos / Universal",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c5/Big_buck_bunny_poster_big.jpg/512px-Big_buck_bunny_poster_big.jpg",
        "url": "https://archive.org/download/BigBuckBunny_124/Content/big_buck_bunny_720p_surround.mp4",
        "desc": "Clássico curta-metragem aberto da Blender Foundation sobre um coelho gigante e esquilos travessos. Licença Creative Commons CC-BY 3.0."
    },
    {
        "id": "Sintel_2010",
        "title": "Sintel (A Busca do Dragão)",
        "year": 2010,
        "group": "Cinema Aberto & Creative Commons",
        "director": "Colin Levy (Blender Foundation)",
        "lang": "en (Áudio) / Universal",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8f/Sintel_poster.jpg/512px-Sintel_poster.jpg",
        "url": "https://archive.org/download/Sintel/sintel-2048-surround.mp4",
        "desc": "Emocionante curta épico de fantasia sobre uma jovem guerreira que resgata um pequeno dragão. Licença Creative Commons CC-BY 3.0."
    },
    {
        "id": "TearsOfSteel_2012",
        "title": "Tears of Steel (Lágrimas de Aço)",
        "year": 2012,
        "group": "Cinema Aberto & Creative Commons",
        "director": "Ian Hubert (Blender Foundation)",
        "lang": "en (Áudio)",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/69/Tears_of_Steel_poster.jpg/512px-Tears_of_Steel_poster.jpg",
        "url": "https://archive.org/download/Tears-of-Steel/tears_of_steel_1080p.mp4",
        "desc": "Ficção científica pós-apocalíptica em Amsterdã combinando atores reais e efeitos visuais abertos em CGI. Licença Creative Commons CC-BY 3.0."
    },
    {
        "id": "ElephantsDream_2006",
        "title": "Elephants Dream (O Sonho dos Elefantes)",
        "year": 2006,
        "group": "Cinema Aberto & Creative Commons",
        "director": "Bassam Kurdali (Blender Foundation)",
        "lang": "en (Áudio)",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/77/Elephants_Dream_poster.jpg/512px-Elephants_Dream_poster.jpg",
        "url": "https://archive.org/download/ElephantsDream/ed_1024.mp4",
        "desc": "O primeiro filme de animação 3D totalmente aberto da história do cinema digital. Licença Creative Commons CC-BY 2.5."
    },
    {
        "id": "CosmosLaundromat_2015",
        "title": "Cosmos Laundromat (Lavanderia Cósmica)",
        "year": 2015,
        "group": "Cinema Aberto & Creative Commons",
        "director": "Mathieu Auvray (Blender Foundation)",
        "lang": "en (Áudio)",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/98/Cosmos_Laundromat_-_Poster.png/512px-Cosmos_Laundromat_-_Poster.png",
        "url": "https://archive.org/download/CosmosLaundromatFirstCycle/Cosmos%20Laundromat%20-%20First%20Cycle%20%281080p%29.mp4",
        "desc": "Em uma ilha desolada, uma ovelha suicida recebe uma oferta para vivenciar infinitas vidas alternativas. Vencedor do prêmio SIGGRAPH. Licença CC-BY."
    }
]

def load_data():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.dirname(script_dir)
    primary_path = os.path.join(root_dir, 'data', 'resolved_archive_items.json')
    extra_path = os.path.join(root_dir, 'data', 'extra_resolved.json')
    anim_path = os.path.join(root_dir, 'data', 'verified_animations_all.json')
    
    with open(primary_path, 'r', encoding='utf-8') as f:
        primary = json.load(f)
    with open(extra_path, 'r', encoding='utf-8') as f:
        extra = json.load(f)
    with open(anim_path, 'r', encoding='utf-8') as f:
        animations = json.load(f)
        
    return primary, extra, animations

def build_catalog():
    primary, extra, animations = load_data()
    script_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.dirname(script_dir)
    catalog_dir = os.path.join(root_dir, 'catalog')
    
    extra_meta = {
        'The Last Man on Earth': ('The Last Man on Earth (Mortos Que Matam)', 1964, 'Terror, Sci-Fi & Cult Clássico', 'Vincent Price', 'en', 'Primeira adaptação do romance Eu Sou a Lenda de Richard Matheson.'),
        'White Zombie': ('White Zombie (Zumbi Branco)', 1932, 'Terror, Sci-Fi & Cult Clássico', 'Bela Lugosi', 'en', 'O primeiro longa-metragem sobre mortos-vivos da história do cinema.'),
        'Meet John Doe': ('Meet John Doe (Adorável Vagabundo)', 1941, 'Clássicos do Cinema Mundial (Drama & Romance)', 'Frank Capra, Gary Cooper, Barbara Stanwyck', 'en', 'Magistral obra de Frank Capra sobre o poder da mídia e a dignidade humana.'),
        'My Man Godfrey': ('My Man Godfrey (Irene, a Teimosa)', 1936, 'Clássicos do Cinema Mundial (Drama & Romance)', 'William Powell, Carole Lombard', 'en', 'Hilariante clássico screwball comedy dos anos 1930.'),
        'The Snows of Kilimanjaro': ('The Snows of Kilimanjaro (As Neves do Kilimanjaro)', 1952, 'Clássicos do Cinema Mundial (Drama & Romance)', 'Gregory Peck, Susan Hayward, Ava Gardner', 'en', 'Baseado no conto de Ernest Hemingway em luxuoso Technicolor.'),
        'Steamboat Bill, Jr.': ('Steamboat Bill, Jr. (Marinheiro de Encomenda)', 1928, 'Comédia & Cinema Mudo', 'Buster Keaton', 'silent', 'Buster Keaton e a lendária cena do ciclone sem dublês.'),
        'Sherlock Jr.': ('Sherlock Jr. (Buster Keaton)', 1924, 'Comédia & Cinema Mudo', 'Buster Keaton', 'silent', 'Projecionista entra dentro do filme dos seus sonhos para desvendar crime.'),
        'The Kid': ('The Kid (O Garoto)', 1921, 'Comédia & Cinema Mudo', 'Charlie Chaplin, Jackie Coogan', 'silent', 'O primeiro longa-metragem dirigido por Chaplin, mesclando humor genial e emoção pura.'),
        'The Gold Rush': ('The Gold Rush (Em Busca do Ouro)', 1925, 'Comédia & Cinema Mudo', 'Charlie Chaplin', 'silent', 'A icônica dança dos pãezinhos e o banquete da bota na corrida do ouro.'),
        'The Vagabond': ('The Vagabond (O Vagabundo)', 1916, 'Comédia & Cinema Mudo', 'Charlie Chaplin, Edna Purviance', 'silent', 'Clássico curta mudo de Chaplin com violino e amor cigano.'),
        'Safety Last!': ('Safety Last! (O Homem Mosca)', 1923, 'Comédia & Cinema Mudo', 'Harold Lloyd', 'silent', 'A célebre cena de Harold Lloyd pendurado nos ponteiros do relógio do edifício.'),
        'D.O.A.': ('D.O.A. (Com as Horas Contadas)', 1950, 'Film Noir, Policial & Mistério', 'Rudolph Maté, Edmond O\'Brien', 'en', 'Homem envenenado corre contra o relógio para desvendar seu próprio assassinato.'),
        'Scarlet Street': ('Scarlet Street (Almas Perversas)', 1945, 'Film Noir, Policial & Mistério', 'Fritz Lang, Edward G. Robinson', 'en', 'Direção precisa de Fritz Lang sobre engano, traição e tragédia moral.'),
        'Detour': ('Detour (Curva do Destino)', 1945, 'Film Noir, Policial & Mistério', 'Edgar G. Ulmer', 'en', 'O mais famoso e influente filme B noir da história do cinema.'),
        'Sherlock Holmes: The Woman in Green': ('Sherlock Holmes: The Woman in Green (A Mulher de Verde)', 1945, 'Film Noir, Policial & Mistério', 'Basil Rathbone, Nigel Bruce', 'en', 'Holmes investiga uma série de assassinatos misteriosos orquestrados pelo Professor Moriarty.'),
        'Sherlock Holmes: Secret Weapon': ('Sherlock Holmes and the Secret Weapon (A Arma Secreta)', 1942, 'Film Noir, Policial & Mistério', 'Basil Rathbone, Nigel Bruce', 'en', 'Holmes e Watson em perigosa missão contra agentes inimigos na 2ª Guerra.'),
        'Angel and the Badman': ('Angel and the Badman (O Anjo e o Bandido)', 1947, 'Faroeste & Western', 'John Wayne, Gail Russell', 'en', 'Pistoleiro foragido acolhido por família pacifista reavalia suas escolhas.'),
        'Trip to the Moon': ('A Trip to the Moon (Viagem à Lua)', 1902, 'Arquivos Históricos & Cinejornais', 'Georges Méliès', 'silent', 'O primeiro clássico de ficção científica da história do cinema mundial.')
    }

    category_mapping = {
        'Terror / Horror': 'Terror, Sci-Fi & Cult Clássico',
        'Terror / Comédia': 'Terror, Sci-Fi & Cult Clássico',
        'Ficção Científica / Cult': 'Terror, Sci-Fi & Cult Clássico',
        'Ficção Científica / Horror': 'Terror, Sci-Fi & Cult Clássico',
        'Ficção Científica / Obra-Prima': 'Terror, Sci-Fi & Cult Clássico',
        'Mistério / Romance': 'Clássicos do Cinema Mundial (Drama & Romance)',
        'Comédia Romântica': 'Clássicos do Cinema Mundial (Drama & Romance)',
        'Drama / Musical': 'Clássicos do Cinema Mundial (Drama & Romance)',
        'Suspense / Noir': 'Film Noir, Policial & Mistério',
        'Film Noir': 'Film Noir, Policial & Mistério',
        'Mistério / Policial': 'Film Noir, Policial & Mistério',
        'Comédia / Ação / Mudo': 'Comédia & Cinema Mudo',
        'Comédia / Mudo': 'Comédia & Cinema Mudo',
        'Comédia': 'Comédia & Cinema Mudo',
        'Western': 'Faroeste & Western',
        'Cinema Brasileiro / Vanguarda': 'Patrimônio do Cinema Brasileiro',
        'Cinema Brasileiro / Clássico': 'Patrimônio do Cinema Brasileiro',
        'Cinema Brasileiro / Histórico': 'Patrimônio do Cinema Brasileiro',
        'Cinema Brasileiro / Documentário': 'Patrimônio do Cinema Brasileiro',
        'Arquivo Histórico / Cinejornal': 'Arquivos Históricos & Cinejornais',
        'Arquivo Histórico / Esporte': 'Arquivos Históricos & Cinejornais',
        'Documentário / Guerra Fria': 'Arquivos Históricos & Cinejornais',
        'Documentário / Futurismo 50s': 'Arquivos Históricos & Cinejornais'
    }

    all_media = []

    # 1. Add Live Channels (30 channels)
    for ch in LIVE_CHANNELS:
        all_media.append({
            "id": ch["id"],
            "title": ch["name"],
            "year": None,
            "group": ch["group"],
            "country": ch.get("country", ""),
            "director": None,
            "lang": ch["lang"],
            "stream_url": ch["url"],
            "logo_url": ch["logo"],
            "ref_logo": ch.get("ref_logo", ""),
            "desc": ch["desc"],
            "type": "live_stream"
        })

    # 2. Add Primary Resolved Cinema & Heritage Items (excluding old animation entries to avoid duplicates)
    for item in primary:
        genre = item.get('genre', '')
        if 'Animação' in genre:
            continue
        group = category_mapping.get(genre, 'Clássicos do Cinema Mundial (Drama & Romance)')
        all_media.append({
            "id": item.get('identifier'),
            "title": item.get('title'),
            "year": item.get('year'),
            "group": group,
            "director": item.get('director'),
            "lang": item.get('lang'),
            "stream_url": item.get('stream_url'),
            "logo_url": item.get('logo_url'),
            "desc": item.get('synopsis'),
            "size_mb": item.get('size_mb'),
            "type": "vod_archive"
        })

    # 3. Add Extra Resolved Items (excluding old animation entries)
    for item in extra:
        name = item.get('name')
        if name not in extra_meta:
            continue
        title, year, group, director, lang, desc = extra_meta[name]
        all_media.append({
            "id": item.get('identifier'),
            "title": title,
            "year": year,
            "group": group,
            "director": director,
            "lang": lang,
            "stream_url": item.get('stream_url'),
            "logo_url": item.get('logo_url'),
            "desc": desc,
            "size_mb": item.get('size_mb'),
            "type": "vod_archive"
        })

    # 4. Add Complete Verified Animation Classics (46 items)
    for anim in animations:
        all_media.append({
            "id": anim["id"],
            "title": anim["title"],
            "year": anim.get("year"),
            "group": "Animações Clássicas de Domínio Público",
            "director": anim.get("director") or anim.get("studio"),
            "lang": anim.get("lang", "en"),
            "stream_url": anim["stream_url"],
            "logo_url": anim["logo_url"],
            "desc": anim.get("desc", ""),
            "size_mb": anim.get("size_mb"),
            "type": "vod_animation"
        })

    # 5. Add Open Cinema (Creative Commons - 5 items)
    for om in OPEN_MOVIES:
        all_media.append({
            "id": om["id"],
            "title": om["title"],
            "year": om["year"],
            "group": om["group"],
            "director": om["director"],
            "lang": om["lang"],
            "stream_url": om["url"],
            "logo_url": om["logo"],
            "desc": om["desc"],
            "type": "vod_open_cinema"
        })

    os.makedirs(catalog_dir, exist_ok=True)

    # Save full JSON database
    json_path = os.path.join(catalog_dir, 'catalog.json')
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(all_media, f, ensure_ascii=False, indent=2)

    # Generate Master M3U8
    master_path = os.path.join(catalog_dir, 'public_domain_master.m3u8')
    generate_m3u8(all_media, master_path, 'Catálogo Oficial de Domínio Público (Master)')

    # Generate Category-Specific M3U8 Playlists
    groups = sorted(list(set(m['group'] for m in all_media)))
    category_slugs = {
        'Canais Públicos & Educativos (Ao Vivo)': '01_canais_publicos_ao_vivo.m3u8',
        'Patrimônio do Cinema Brasileiro': '02_patrimonio_brasileiro.m3u8',
        'Arquivos Históricos & Cinejornais': '03_arquivos_historicos_cinejornais.m3u8',
        'Clássicos do Cinema Mundial (Drama & Romance)': '04_cinema_mundial_drama_romance.m3u8',
        'Terror, Sci-Fi & Cult Clássico': '05_terror_scifi_cult.m3u8',
        'Comédia & Cinema Mudo': '06_comedia_cinema_mudo.m3u8',
        'Film Noir, Policial & Mistério': '07_film_noir_policial_misterio.m3u8',
        'Faroeste & Western': '08_faroeste_western.m3u8',
        'Animações Clássicas de Domínio Público': '09_animacoes_classicas.m3u8',
        'Cinema Aberto & Creative Commons': '10_cinema_aberto_creative_commons.m3u8'
    }

    for group_name in groups:
        cat_items = [m for m in all_media if m['group'] == group_name]
        filename = category_slugs.get(group_name, f"cat_{group_name.replace(' ', '_').lower()}.m3u8")
        filepath = os.path.join(catalog_dir, filename)
        generate_m3u8(cat_items, filepath, f"Domínio Público - {group_name}")

    print(f"\n==========================================")
    print(f"Catalog Build Complete!")
    print(f"Total Entries: {len(all_media)}")
    print(f"Categories: {len(groups)}")
    for g in groups:
        count = len([m for m in all_media if m['group'] == g])
        print(f" - {g}: {count} itens")
    print(f"==========================================")

def generate_m3u8(items, filepath, playlist_title):
    lines = [
        "#EXTM3U",
        f"#PLAYLIST:{playlist_title}",
        "#EXT-X-VERSION:3",
        ""
    ]
    for item in items:
        tvg_id = item.get('id', '')
        title = item.get('title', '')
        year_str = f" ({item.get('year')})" if item.get('year') else ""
        full_display_title = f"{title}{year_str}"
        group = item.get('group', 'Domínio Público')
        logo = item.get('logo_url', '')
        stream_url = item.get('stream_url', '')
        lang = item.get('lang', '')
        country = item.get('country', '')
        
        extinf_parts = [
            f'#EXTINF:-1 tvg-id="{tvg_id}"',
            f'tvg-name="{full_display_title}"',
            f'tvg-logo="{logo}"',
            f'group-title="{group}"'
        ]
        if lang:
            extinf_parts.append(f'tvg-language="{lang}"')
        if country:
            extinf_parts.append(f'tvg-country="{country}"')
        
        extinf_line = " ".join(extinf_parts) + f",{full_display_title}"
        lines.append(extinf_line)
        lines.append(f"#EXTGRP:{group}")
        lines.append(stream_url)
        lines.append("")

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write("\n".join(lines))
    print(f"Generated: {filepath} ({len(items)} items)")

if __name__ == '__main__':
    build_catalog()
