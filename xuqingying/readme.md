页面的主要三个功能在control_relation文件内。
  1：查控制关联界面：输入待查询的两实体，输出是否关联控制（控制权大小）
   controlAB=ControlAB('常玉英','交通银行股份有限公司')
   AB=controlAB.data_process()（控制权大小）
   print(AB)
   exist=controlAB.exist（路径是否存在）
   print(exist)
   control=controlAB.cotntrol（二者是否是控制关系）
   print(control)

2：查控制权所属页面：输入实体，输出父节点子图以及对应的控制权大小
    controlA=ControlA('上海山阳电讯器材厂')
    data=controlA.data_process(1)#向外提取一层（参数表示提取子图层数）
    print(data)

3：控制系查询：输入实体，输出其控制系
    #controlB=ControlFull('常玉英')
    #B=controlB.data_process(1)#向内提取一层（参数表示提取子图层数）
    #print(B)
