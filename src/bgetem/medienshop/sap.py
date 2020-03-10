from sapshopapi import sapshopapi
from sapshopapi import interfaces
from zope import component, interface


@interface.implementer(interfaces.ISAPShopConnection)
class Connection(sapshopapi.SAPAPI):
    """ Example Connection """


#def setup_sap_connection():
#    """ setup any state specific to the execution of the given module."""
#    connection = Connection(
#        BASE_URL="http://SVASAPXQAS.BG10.BGFE.LOCAL:8000/sap/bc/srt/wsdl/flv_10002P111AD1/sdef_url/",
#        SEARCH_URL="zws_etemweb_suche/050/zws_etemweb_suche/zws_etemweb_suche?sap-client=050",
#        ITEM_URL="zws_etem_imp_artikel/050/zws_etem_imp_artikel/zws_etem_imp_artikel?sap-client=050",
#        ALL_ITEMS_URL="zws_etem_imp_all_items/050/zws_etem_imp_all_items/zws_etem_imp_all_items?sap-client=050"
#    )
#    return connection

#def setup_sap_connection():
#    """ setup any state specific to the execution of the given module."""
#    connection = Connection(
#        BASE_URL="http://SVASAPXQAS.BG10.BGFE.LOCAL:8000/sap/bc/srt/wsdl/flv_10002P111AD1/sdef_url/",
#        SEARCH_URL="zws_etemweb_suche/050/zws_etemweb_suche/zws_etemweb_suche?sap-client=050",
#        ITEM_URL="ZWS_ETEM_IMP_ARTIKEL?sap-client=050",
#        ALL_ITEMS_URL="ZWS_ETEM_IMP_ALL_ITEMS?sap-client=050"
#    )
#    return connection

#def setup_sap_connection():
#    """ setup any state specific to the execution of the given module."""
#    connection = Connection(
#        BASE_URL="http://SVASAPXQAS.BG10.BGFE.LOCAL:8000/sap/bc/srt/wsdl/flv_10002A111AD1/srvc_url/sap/bc/srt/rfc/sap/",
#        ITEM_URL="zws_etem_imp_artikel/050/zws_etem_imp_artikel/zws_etem_imp_artikel?sap-client=050",
#        ALL_ITEMS_URL="zws_etem_imp_all_items/050/zws_etem_imp_all_items/zws_etem_imp_all_items?sap-client=050",
#        ADD_USER_URL="zws_etem_imp_create_user/050/zws_etem_imp_create_user/zws_etem_imp_create_user?sap-client=050",
#        UPDATE_USER_URL="zws_etem_imp_update_user/050/zws_etem_imp_update_user/zws_etem_imp_update_user?sap-client=050",
#        GET_USER_URL="zws_etem_imp_get_user/050/zws_etem_imp_get_user/zws_etem_imp_get_user?sap-client=050",
#        DELETE_USER_URL="zws_etem_imp_delete_user_req/050/zws_etem_imp_delete_user_req/zws_etem_imp_delete_user_req?sap-client=050",
#        DELETE_USER_URLV="zws_etem_imp_delete_user_ver/050/zws_etem_imp_delete_user_ver/zws_etem_imp_delete_user_ver?sap-client=050",
#        UPDATE_PASSWORD_URL="zws_etem_imp_update_password/050/zws_etem_imp_update_password/zws_etem_imp_update_password?sap-client=050",
#        RESET_PASSWORD_URL="zws_etem_imp_reset_password/050/zws_etem_imp_reset_password/zws_etem_imp_reset_password?sap-client=050",
#        GET_PASSWORD_URL="zws_etem_imp_get_password/050/zws_etem_imp_get_password/zws_etem_imp_get_password?sap-client=050",
#        CREATE_ORDER_URL="zws_etem_imp_create_order/050/zws_etem_imp_create_order/zws_etem_imp_create_order?sap-client=050"
#    )
#    return connection

def setup_sap_connection():
    """ setup any state specific to the execution of the given module."""
    connection = Connection(
        BASE_URL="http://SVASAPXPRD.BG10.BGFE.LOCAL:8000/sap/bc/srt/wsdl/flv_10002A111AD1/bndg_url/sap/bc/srt/rfc/sap/",
        ITEM_URL="zws_etem_imp_artikel/050/zws_etem_imp_artikel/zws_etem_imp_artikel?sap-client=050",
        ALL_ITEMS_URL="zws_etem_imp_all_items/050/zws_etemweb_all_items/zws_etemweb_all_items?sap-client=050",
        ADD_USER_URL="zws_etem_imp_create_user/050/zws_etem_imp_create_user/zws_etem_imp_create_user?sap-client=050",
        UPDATE_USER_URL="zws_etem_imp_update_user/050/zws_etem_imp_update_user/zws_etem_imp_update_user?sap-client=050",
        GET_USER_URL="zws_etem_imp_get_user/050/zws_etem_imp_get_user/zws_etem_imp_get_user?sap-client=050",
        DELETE_USER_URL="zws_etem_imp_delete_user_req/050/zws_etem_imp_delete_user_req/zws_etem_imp_delete_user_req?sap-client=050",
        DELETE_USER_URLV="zws_etem_imp_delete_user_ver/050/zws_etem_imp_delete_user_ver/zws_etem_imp_delete_user_ver?sap-client=050",
        UPDATE_PASSWORD_URL="zws_etem_imp_update_password/050/zws_etem_imp_update_password/zws_etem_imp_update_password?sap-client=050",
        RESET_PASSWORD_URL="zws_etem_imp_reset_password/050/zws_etem_imp_reset_password/zws_etem_imp_reset_password?sap-client=050",
        GET_PASSWORD_URL="zws_etem_imp_get_password/050/zws_etem_imp_get_password/zws_etem_imp_get_password?sap-client=050",
        CREATE_ORDER_URL="zws_etem_imp_create_order/050/zws_etem_imp_create_order/zws_etem_imp_create_order?sap-client=050"
    )
    return connection
