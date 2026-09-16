import Feature22Domain

public enum Feature22DataRepository {
    public static func load(_ id: Int) -> Feature22DomainModel {
        Feature22DomainModel(id: id, title: "Feature 22")
    }
}
