# coding=utf-8

import uuid
import utils
import random
import datetime
import psycopg2 as ps

from mistral import MistralAi
from ai_interface import AiTarget
from ai_interface import AiInterface

__images_url = None
__review_prompt_id = None
__active_community_status = 1
__publications_prompt_id = None

def getUrlForImages() -> str:
    global __images_url
    if __images_url is not None:
        return str(__images_url)
    consul = utils.__getConsulProvider()
    if consul is None:
        return "https://business-ai/hooded/assortment/images/"
    result = utils.__getConsulProvider().kv.get('business_ai.imagesUrl')[1]
    if result is None:
        result = "https://business-ai/hooded/assortment/images/"
        utils.__getConsulProvider().kv.put('business_ai.imagesUrl', result)
    else:
        result = result['Value'].decode('UTF-8')
    return result

def getAiProvider(organization: str, target: AiTarget) -> AiInterface:
    return MistralAi()

def getPublicationsPromptId(organization: str) -> str:
    global __publications_prompt_id
    if __publications_prompt_id is not None:
        return __publications_prompt_id
    consul = utils.__getConsulProvider()
    if consul is None:
        __publications_prompt_id = str(uuid.uuid4())
        return __publications_prompt_id
    result = utils.__getConsulProvider().kv.get('business_ai.publications_prompt_id')[1]
    if result is None:
        result = str(uuid.uuid4())
        utils.__getConsulProvider().kv.put('business_ai.publications_prompt_id', result)
    else:
        result = result['Value'].decode('UTF-8')
    __publications_prompt_id = result
    return result

def getPromptForPublication(organization: str) -> str:
    try:
        conn = ps.connect(utils.getDbUrl())
        with conn.cursor() as cursor:
            cursor.execute("SELECT fcontent FROM " + utils.getBusinessDbSchema() +
                           ".prompts WHERE id = '" + getPublicationsPromptId(organization) + "'")
            result = cursor.fetchone()
            if result[0] is None:
                return ""
            return result[0]
    except Exception as e:
        print(utils.dbConnectionError + f": {e}")
        return ""

def getReviewPromptId(organization: str) -> str:
    global __review_prompt_id
    if __review_prompt_id is not None:
        return __review_prompt_id
    consul = utils.__getConsulProvider()
    if consul is None:
        __review_prompt_id = str(uuid.uuid4())
        return __review_prompt_id
    result = utils.__getConsulProvider().kv.get('business_ai.review_prompt_id')[1]
    if result is None:
        result = str(uuid.uuid4())
        utils.__getConsulProvider().kv.put('business_ai.review_prompt_id', result)
    else:
        result = result['Value'].decode('UTF-8')
    __review_prompt_id = result
    return result

def getPromptForReview(organization: str) -> str:
    try:
        conn = ps.connect(utils.getDbUrl())
        with conn.cursor() as cursor:
            cursor.execute("SELECT fcontent FROM " + utils.getBusinessDbSchema() +
                           ".prompts WHERE id = '" + getReviewPromptId(organization) + "'")
            result = cursor.fetchone()
            if result[0] is None:
                return ""
            return result[0]
    except Exception as e:
        print(utils.dbConnectionError + f": {e}")
        return ""

def askDisposer(organization: str) -> bool:
    try:
        conn = ps.connect(utils.getDbUrl())
        with conn.cursor() as cursor:
            cursor.execute("SELECT max(p.created_at) FROM " + utils.getBusinessDbSchema() +
                           ".publications p INNER JOIN " + utils.getBusinessDbSchema() +
                           ".organization o ON p.organization_id = o.id WHERE o.strictname = '" + organization + "'")
            created = cursor.fetchone()
            if created[0] is None:
                return True
            return (datetime.datetime.now() - created[0]).total_seconds() > utils.getPublicationsInterval()
    except Exception as e:
        print(utils.dbConnectionError + f": {e}")
        return False

def getAssortmentForPublication(organization: str):
    conn = ps.connect(utils.getDbUrl())
    with conn.cursor() as cursor:
        assortments = []
        cursor.execute("SELECT a.id, a.fname, a.description FROM " + utils.getBusinessDbSchema() +
                       ".assortment a INNER JOIN " + utils.getBusinessDbSchema() +
                       ".organization o ON a.manufacturer = o.id WHERE o.strictname = '" + organization + "'")
        for row in cursor.fetchall():
            assortments.append(row)
        return assortments[random.randint(0, len(assortments) - 1)]

def getImageForPublication(assortment: uuid) -> str:
    conn = ps.connect(utils.getDbUrl())
    with conn.cursor() as cursor:
        images = []
        cursor.execute("SELECT images FROM " + utils.getBusinessDbSchema() +
                       ".ass_image WHERE assortment_id = '" + assortment + "'")
        for row in cursor.fetchall():
            images.append(row)
        return images[random.randint(0, len(images) - 1)]

def generatePublication(organization: str):
    print(f"Generate publication for {organization}")
    if askDisposer(organization):
        provider = getAiProvider(organization, AiTarget.publication)
        assortment = getAssortmentForPublication(organization)
        imageUrl = getUrlForImages() + assortment[0] + "/"
        imageName = getImageForPublication(assortment[0])
        publication = provider.generate_publication(imageUrl + imageName[0], organization,
                      assortment[1], assortment[2], getPromptForPublication(organization))
        if publication is None:
            return
        try:
            conn = ps.connect(utils.getDbUrl())
            with conn.cursor() as cursor:
                cursor.execute("SELECT id FROM " + utils.getDbSchema() +
                               ".organization WHERE strictname = '" + organization + "'")
                orgId = cursor.fetchone()
                timeCreated = str(datetime.datetime.now())
                cursor.execute("INSERT INTO " + utils.getDbSchema() + ".publications(created_at, organization_id, "
                               "assortment_id, prompt_id, fcontent, fstate) VALUES('" + timeCreated +
                                "', '" + orgId[0] + "', '" + assortment[0] + "', '" +
                                getPublicationsPromptId(organization) + "', '" +
                                publication + "', 0)")
                cursor.execute("INSERT INTO " + utils.getDbSchema() + ".publication_images(publications_created_at,"
                               "publications_organization_id, images) VALUES('" + timeCreated + "', '" + orgId[0] +
                               "', '" + imageName[0] + "')")
                conn.commit()
        except Exception as e:
            print(f": {e}")

def selectNewRequests(organization: str):
    try:
        conn = ps.connect(utils.getDbUrl())
        with conn.cursor() as cursor:
            cursor.execute("SELECT r.created_at, r.organization_id, r.client, r.frate, r.platform, r.request_text "
                           "FROM " + utils.getDbSchema() + ".cust_requests r INNER JOIN " +  utils.getDbSchema() +
                           ".organization o ON r.organization_id = o.id WHERE o.strictname = '" + organization +
                           "' AND r.fstate = 0")
            return cursor.fetchall()
    except Exception as e:
        print(f": {e}")
        return []

def processClientRequests(organization: str):
    print(f"Process client requests for {organization}")
    provider = getAiProvider(organization, AiTarget.response)
    requests = selectNewRequests(organization)
    prompt = getPromptForReview(organization)
    for request in requests:
        answer = provider.response_to_request(organization, request[5], prompt)
        if answer is None:
            continue
        try:
            conn = ps.connect(utils.getDbUrl())
            with conn.cursor() as cursor:
                cursor.execute("UPDATE " + utils.getDbSchema() + ".cust_requests SET fstate = 1, answer_text = '" +
                               answer + "', prompt_id = '" + getReviewPromptId(organization) + "', ai_provider = '" +
                               provider.getId() + "' WHERE created_at = '" + str(request[0]) + "' AND organization_id = '" +
                               request[1] + "' AND client = '" + request[2] + "'")
            conn.commit()
        except Exception as e:
            print(f": {e}")

def businessAiProcessing():
    global __active_community_status
    try:
        conn = ps.connect(utils.getDbUrl())
        with conn.cursor() as cursor:
            cursor.execute("SELECT fname FROM " + utils.getDbSchema() +
                           ".community WHERE fapp = '" + utils.getApplicationName() +
                           "' AND status = " + str(__active_community_status))
            for community in cursor.fetchall():
                processClientRequests(community[0])
                generatePublication(community[0])
    except Exception as e:
        print(f"{e}")

businessAiProcessing()
