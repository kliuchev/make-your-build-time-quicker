import Feature30Domain

public enum Feature30DataRepository {
    public static func load(_ id: Int) -> Feature30DomainModel {
        Feature30DomainModel(id: id, title: "Feature 30")
    }
}
