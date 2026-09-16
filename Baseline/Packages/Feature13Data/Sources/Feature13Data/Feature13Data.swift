import Feature13Domain

public enum Feature13DataRepository {
    public static func load(_ id: Int) -> Feature13DomainModel {
        Feature13DomainModel(id: id, title: "Feature 13")
    }
}
