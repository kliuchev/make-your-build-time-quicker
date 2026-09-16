import Feature25Domain

public enum Feature25DataRepository {
    public static func load(_ id: Int) -> Feature25DomainModel {
        Feature25DomainModel(id: id, title: "Feature 25")
    }
}
