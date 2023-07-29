
import { request } from '@/api/service'
export const urlPrefix = '/api/crawler/system_var/'

export function sendSubMsg (data) {
  return request({
    url: urlPrefix + 'send_msg/',
    method: 'POST',
    data: data
  })
}
