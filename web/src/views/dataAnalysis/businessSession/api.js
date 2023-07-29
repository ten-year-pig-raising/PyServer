import { request } from "@/api/service";
export const urlPrefix = "/api/crawler/business_session/";

export function GetList(query) {
  return request({
    url: urlPrefix,
    method: "get",
    params: query,
  });
}

export function AddObj(obj) {
  return request({
    url: urlPrefix,
    method: "post",
    data: obj,
  });
}

export function UpdateObj(obj) {
  return request({
    url: urlPrefix + obj.id + "/",
    method: "put",
    data: obj,
  });
}

export function DelObj(id) {
  return request({
    url: urlPrefix + id + "/",
    method: "delete",
    data: { id },
  });
}

export function getShopComments(data) {
  return request({
    url: urlPrefix + "get_shop_comments/",
    method: "POST",
    data: data,
  });
}
