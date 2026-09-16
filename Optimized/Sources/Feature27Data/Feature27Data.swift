import Feature27Domain

public enum Feature27DataRepository {
    public static func load(_ id: Int) -> Feature27DomainModel {
        Feature27DomainModel(id: id, title: "Feature 27")
    }
}
