#-*- coding: UTF-8 -*-
from app import db
from app.models import ComName, User, Acachemy, Role, Teacher

def createdb():
    db.drop_all()
    db.create_all()
    Role.insert_roles()
    admin_role = Role.query.filter_by(name='Administrator').first()
    admin = User('admin', u'管理员')
    admin.password = '123'
    admin.role = admin_role

    teacher_role = Role.query.filter_by(name='Teacher').first()
    teacher = User('T00001', u'老师')
    teacher.password = '123'
    teacher.role = teacher_role
    
    db.session.add_all([admin, teacher])
    db.session.commit()
    
    aca = [
    u'机械工程学院',
    u'交通与车辆工程学院',
    u'农业工程与食品科学学院',
    u'电气与电子工程学院',
    u'计算机科学与技术学院',
    u'化学工程学院',
    u'建筑工程学院',
    u'资源与环境工程学院',
    u'材料科学与工程学院',
    u'生命科学学院',
    u'理学院',
    u'商学院',
    u'文学与新闻传播学院',
    u'外国语学院',
    u'法学院',
    u'马克思主义学院',
    u'美术学院',
    u'音乐学院',
    u'体育学院',
    u'国防教育学院',
    u'鲁泰纺织服装学院']
    
    for a in aca:
        Aca = Acachemy(a)
        db.session.add(Aca)
        db.session.commit()

    tea = [
    (u'艾兵', u'化学工程院'),
    (u'安春艳', u'生命科学院'),
    (u'安琳', u'农业食品院'),
    (u'巴奉丽', u'电子电气院')]

    tea_id = User.query.filter_by(role=teacher_role).order_by().first().user_id
    id = int(tea_id[1:])
        
    for t in tea:
        id += 1
        T = str('T'+'%05d' %id)
        Tea = User(T,t[0])
        Tea.password = '123'
        Tea.role = teacher_role
        db.session.add(Tea)
        db.session.commit()
        
    for t in tea:
        tea_id = User.query.filter_by(user_name=t[0]).first().id
        Tea = Teacher(tea_id,t[0],t[1])
        db.session.add(Tea)
        db.session.commit()

    com = [
    u'“挑战杯”全国大学生课外学术科技作品竞赛',
    u'“挑战杯”山东省大学生创业计划竞赛',
    u'国际大学生数学建模竞赛',
    u'全国大学生数学建模竞赛',
    u'全国大学生电工数学建模竞赛',
    u'全国大学生电子设计竞赛',
    u'全国大学生工程训练综合能力竞赛',
    u'全国大学生机械设计创新大赛',
    u'山东省大学生机电产品创新设计竞赛',
    u'全国大学生广告艺术大赛',
    u'全国信息技术应用水平大赛',
    u'“高教杯”全国大学生先进成图技术与产品信息建模创新大赛',
    u'“博创杯”全国大学生嵌入式物联网设计大赛',
    u'全国大学生农业建筑环境与能源工程相关专业创新设计竞赛',
    u'全国高等院校“广联达杯”工程算量大赛',
    u'全国大学生测绘科技论文竞赛',
    u'中国大学生铸造工艺设计大赛',
    u'中国机器人大赛暨robocup公开赛',
    u'全国三维数字化创新设计大赛',
    u'全国大学生“飞思卡尔”杯智能汽车竞赛',
    u'全国大学生化工设计竞赛',
    u'山东省大学生化学实验技能竞赛',
    u'全国大学生节能减排社会实践与科技竞赛',
    u'齐鲁软件大赛',
    u'山东省ACM大学生程序设计竞赛',
    u'山东省大学生建筑设计大赛',
    u'山东省大学生结构设计大赛',
    u'中国大学生高分子材料创新创业大赛',
    u'全国高等学校大学生测绘技能竞赛',
    u'全国大学生工业设计大赛',
    u'山东省大学生电子与信息技术应用水平大赛',
    u'山东省大学生物理科技创新大赛',
    u'山东省大学生物理教学技能大赛',
    u'全国大学生数学竞赛',
    u'全国大学生英语竞赛',
    u'“外研社杯”全国英语演讲大赛',
    u'山东省大学生科技外语大赛',
    u'全国大学生英语风采大赛',
    u'全国大学生英语演讲比赛',
    u'全国大学生网络商务创新应用大赛',
    u'齐鲁大学生创业计划竞赛',
    u'高校环保科技创意设计大赛',
    u'山东省师范类高校学生从业技能大赛',
    u'山东省高校音乐专业师生基本功比赛',
    u'山东省体育教育专业大学生基本功大赛',
    u'山东省大学生足球锦标赛',
    u'山东省大学生篮球锦标赛',
    u'山东省高校美术与设计专业基本功比赛',
    u'山东省服装面料图案设计大赛']

    for c in com:
        Com = ComName(c)
        db.session.add(Com)
        db.session.commit()

if __name__ == '__main__':
    createdb()
