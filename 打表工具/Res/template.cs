[Script]
using System.Collections.Generic;
using System;

public class $className : CSVData
{
    private static readonly string s_TableName = "$fileName";

    private static readonly $className s_instance = new $className();
    public static $className instance { get {return s_instance; } }

    private static Dictionary<byte[], $className> s_DataDict = new Dictionary<byte[], $className>();

    #region 定义字段
    $defineField
    #endregion

    #region Override

    protected override string Name()
    {
        return s_TableName;
    }

    public override void UnloadData(bool isRemove = true)
    {
        base.UnloadData(isRemove);
        s_DataDict.Clear();

        // 清除缓存
        if (isRemove)
            CSVManager.instance.RemoveCSVData(Name());
    }

    #endregion

    #region 功能函数

    /// <summary>
    /// 通过key获取对象
    /// </summary>
    private $className Get(byte[] key, bool isCache = true)
    {
        LoadCSVTable();

        $className csvData;
        if (!s_DataDict.TryGetValue(key, out csvData))
        {
            CSVBytesData bytesData = GetCSVBytesData(key);
            if (bytesData == null)
                return null;
            csvData = GetCSVData(bytesData);
            if (isCache)
            {
                if (!s_DataDict.ContainsKey(key))
                    s_DataDict.Add(key, csvData);
            }
        }
        return csvData;
    }

    private $className GetCSVData(CSVBytesData bytesData)
    {
        $className csvData = null;
        try
        {
            csvData = new $className();
            csvData.bytesData = bytesData;
            bytesData.BeginLoad();

            // 读取字段
$readField
        }
        catch (Exception exception)
        {
            UnityEngine.Debug.LogErrorFormat("{0}表 解析出错 {1}", s_TableName, exception.StackTrace);
            return null;
        }

        return csvData;
    }

    private Dictionary<byte[], $className> GetAll(bool isCache)
    {
        LoadCSVTable();

        Dictionary<byte[], $className> allDict = new Dictionary<byte[], $className>();
        if (s_DataDict.Count == GetAllCSVBytesData().Count)
        {
            allDict = s_DataDict;
        }
        else
        {
            s_DataDict.Clear();
            var iter = GetAllCSVBytesData().GetEnumerator();
            while (iter.MoveNext())
            {
                $className csvData = Get(iter.Current.Key);
                allDict.Add(iter.Current.Key, csvData);
            }
            iter.Dispose();

            if (isCache)
                s_DataDict = allDict;
        }
        return allDict;
    }

    #endregion

    #region 静态函数

    public static Dictionary<byte[], $className> GetAllDict(bool isCache = false)
    {
        return instance.GetAll(isCache);
    }

    public static void Load()
    {
        instance.LoadCSVTable();
    }

    public static void Unload(bool isRemove = true)
    {
        instance.UnloadData(isRemove);
    }

    #endregion
}
[Script]

[BaseProperty]
    /// <summary>
    /// $destribe
    /// </summary>
    public $attrtype $attrname { private set; get; }
[BaseProperty]

[ReadBaseProperty]
            csvData.$attrname = bytesData.Read$attrtype();
[ReadBaseProperty]
