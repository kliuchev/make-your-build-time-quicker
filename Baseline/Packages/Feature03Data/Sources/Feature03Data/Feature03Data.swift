import Feature03Domain

public enum Feature03DataRepository {
    public static func load(_ id: Int) -> Feature03DomainModel {
        Feature03DomainModel(id: id, title: "Feature 3")
    }
}
