package models

import (
	"time"
)

type Model struct {
	ID         uint      `gorm:"primarykey"`
	CreateTime time.Time `gorm:"autoCreateTime"`
	UpdateTime time.Time `gorm:"autoUpdateTime"`
	DeptBelong uint
	Creator    uint
}
type Dept struct {
	Name     string `gorm:"size:255;not null;comment:部门名称;"`
	Key      string `gorm:"size:255;not null;comment:部门标识;"`
	ParentId uint   `gorm:"comment:父级部门;"`
	Parent   *Dept  `gorm:"foreignKey:ParentId;references:ID;"`
	Sort     int    `gorm:"comment:排序;"`
	Owner    string
	Model
}

func (u *Dept) TableName() string { // 数据库表名
	return "dept"
}

type User struct {
	Name     string `gorm:"size:255;"`
	Username string `gorm:"size:255;index;unique;not null;comment:用户名;"`
	Password string `gorm:"size:255;not null;comment:密码;"`
	Age      int    `gorm:"type:int;"`
	Role     JSON   `gorm:"comment:角色;"`
	DeptId   uint   `gorm:"comment:所属部门;"`
	Dept     Dept   `gorm:"foreignKey:ID;references:DeptId;"`
	Type     int
	Model
}

func (u *User) TableName() string { // 数据库表名
	return "user"
}

type Menu struct {
	ParentId  uint   `gorm:"comment:父级菜单;"`
	Parent    *Menu  `gorm:"foreignKey:ParentId;references:ID;"`
	Icon      string `gorm:"size:255;comment:图标;"`
	Label     string `gorm:"size:255;comment:菜单名称;"`
	Sort      string `gorm:"size:255;comment:菜单排序;"`
	IsLink    bool   `gorm:"default:false;comment:是否链接;"`
	IsCatlog  bool   `gorm:"default:false;comment:菜单目录;"`
	Name      string `gorm:"size:255;comment:路由名称;"`
	Path      string `gorm:"size:255;comment:路由地址;"`
	Component string `gorm:"size:255;comment:组件地址;"`
	Disabled  bool   `gorm:"default:false;comment:是否禁用;"`
	Cache     bool   `gorm:"default:false;comment:是否缓存;"`
	Model
}

func (u *Menu) TableName() string { // 数据库表名
	return "menu"
}

type MenuInterface struct {
	Name   string `gorm:"size:255;comment:接口名称;"`
	Key    string `gorm:"size:255;not null;comment:接口标识;"`
	Method int    `gorm:"size:255;comment:请求方式;"`
	Path   string `gorm:"size:255;comment:接口地址;"`
	MenuId uint   `gorm:"comment:所属菜单;"`
	Menu   Menu   `gorm:"foreignKey:MenuId;references:ID;"`
	Model
}

func (u *MenuInterface) TableName() string { // 数据库表名
	return "menu_interface"
}

type Role struct {
	Name          string          `gorm:"size:255;comment:角色名称;"`
	Key           string          `gorm:"size:255;not null;comment:角色标识;"`
	Permisson     int             `gorm:"size:255;comment:请求方式;"`
	Menu          []Menu          `gorm:"many2many:role_menu;"`
	MenuInterface []MenuInterface `gorm:"many2many:role_menu_interface;"`
	IsAdmin       bool            `gorm:"default:false;comment:是否管理员;"`
	Model
}

func (u *Role) TableName() string { // 数据库表名
	return "role"
}

type Area struct {
	Name     string  `gorm:"size:255;not null;comment:名称;"`
	Code     string  `gorm:"size:255;not null;comment:编码;"`
	Level    int     `gorm:"not null;comment:地区等级;"`
	Lat      float64 `gorm:"comment:纬度;"`
	Lng      float64 `gorm:"comment:经度;"`
	ParentId uint    `gorm:"comment:父级区域;"`
	Parent   *Area   `gorm:"foreignKey:ParentId;references:ID;"`
	Model
}

func (u *Area) TableName() string { // 数据库表名
	return "area"
}

type Log struct {
	Username        string `gorm:"size:255;comment:登录用户名;"`
	Ip              string `gorm:"size:255;comment:登录ip;"`
	Agent           string `gorm:"size:255;comment:agent信息;"`
	Browser         string `gorm:"size:255;comment:浏览器名;"`
	Os              string `gorm:"size:255;comment:操作系统;"`
	Continent       string `gorm:"size:255;comment:州;"`
	Country         string `gorm:"size:255;comment:国家;"`
	Province        string `gorm:"size:255;comment:省份;"`
	City            string `gorm:"size:255;comment:城市;"`
	District        string `gorm:"size:255;comment:县区;"`
	Isp             string `gorm:"size:255;comment:运营商;"`
	Area_code       string `gorm:"size:255;comment:区域代码;"`
	Country_english string `gorm:"size:255;comment:英文全称;"`
	Country_code    string `gorm:"size:255;comment:简称;"`
	Longitude       string `gorm:"size:255;comment:经度;"`
	Latitude        string `gorm:"size:255;comment:纬度;"`
	Login_type      int    `gorm:"comment:登录类型;"`
	Model
}

func (u *Log) TableName() string { // 数据库表名
	return "log"
}

type File struct {
	Name string `gorm:"size:255;not null;comment:文件名;"`
	Url  string `gorm:"size:255;not null;comment:文件路径;"`
	Model
}

func (u *File) TableName() string { // 数据库表名
	return "file"
}

type Article struct {
	Name    string    `gorm:"size:255;not null;comment:名称;"`
	Source  string    `gorm:"size:255;comment:来源;"`
	Content string    `gorm:"comment:内容;"`
	Url     string    `gorm:"size:255;not null;comment:链接;"`
	UrlHash string    `gorm:"size:255;not null;comment:链接哈希值;"`
	PubTime time.Time `gorm:"comment:发布时间;"`
	Model
}

func (u *Article) TableName() string { // 数据库表名
	return "article"
}
