import Feature16Domain

public enum Feature16DataRepository {
    public static func load(_ id: Int) -> Feature16DomainModel {
        Feature16DomainModel(id: id, title: "Feature 16")
    }
}
