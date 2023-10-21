<script>
import qs from 'qs'
import store from './store';
export default {
  onLaunch: function () {
    uni.addInterceptor('request', {
      invoke(args) {
        const {
          data,
          method,
        } = args;
        if (method === "GET") {
          // TODO:params arr=[1,2] 数组转 arr=1&arr=2 
          // 如果是get请求，且params是数组类型如arr=[1,2]，则转换成arr=1&arr=2  ------  npm install qs
          const newData = qs.stringify(data, {
            arrayFormat: "repeat"
          })
          delete args.data;
          args.url = `${args.url}?${newData}`;
        }
        if (uni.getStorageSync("access")) {
          store().is_login = true
        }
      },
      success(args) {
        // 请求成功后，修改code值为1
        if (args.statusCode == 401) {
          console.log('401----------------------', args)
          uni.clearStorageSync()
          uni.redirectTo({
            url: '/pages/login/index'
          });
        }
        else if (args.statusCode == 599) {
          uni.clearStorageSync()
        }
      },
      fail(err) {
        console.log('请求出错 ', err);
        uni.clearStorageSync()
      },
      complete(res) {
        // console.log('interceptor-complete', res)
      }
    })
  },
  onShow: function () {
    console.log('App Show')
  },
  onHide: function () {
    console.log('App Hide')
  },
}
</script>

<style lang="scss">
@import "./uni_modules/vk-uview-ui/index.scss";
</style>
