package tools

func Keys(m map[string]interface{}) []string {
	r := make([]string, len(m))
	index := 0
	for k := range m {
		r[index] = k
		index++
	}
	return r
}

func DeleteSlice(slice []string, value string) []string {
	j := 0
	for _, v := range slice { // 切片循环
		if v != value { //按值删除
			slice[j] = v
			j++
		}
	}
	return slice[:j]
}

func Contains(arr []string, item string) bool {
	for _, v := range arr {
		if v == item {
			return true
		}
	}
	return false
}
